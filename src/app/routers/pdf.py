"""
PDF router — handles both digital PDF and scanned PDF uploads.
- Digital PDF: synchronous, returns JSON OcrResult.
- Scanned PDF: streams SSE events per page, saves DB after done.
"""
import json
import logging
from collections.abc import AsyncGenerator

from fastapi import APIRouter, BackgroundTasks, UploadFile, File, status
from fastapi.responses import StreamingResponse

from app.core.dependencies import DBSession
from app.schemas.ocr_job import OcrResult
from app.services.ocr_service import ocr_job_service
from app.utils.file_utils import (
    read_and_validate_upload,
    save_temp_file,
    delete_temp_file,
    ALLOWED_PDF_MIME,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/pdf", tags=["PDF"])


@router.post(
    "/digital",
    response_model=OcrResult,
    status_code=status.HTTP_200_OK,
    summary="Upload PDF văn bản → Markdown",
    description="Chuyển đổi PDF có text layer (digital PDF) sang Markdown bằng pymupdf4llm.",
)
async def upload_digital_pdf(
    file: UploadFile = File(..., description="File PDF văn bản (≤ 50MB)"),
    db: DBSession = None,
):
    content = await read_and_validate_upload(file, ALLOWED_PDF_MIME)
    file_path = save_temp_file(content, file.filename or "upload.pdf")

    try:
        from app.ocr_engine.pipeline import run_digital_pdf_pipeline

        result_md, page_count = run_digital_pdf_pipeline(file_path)
        logger.info("✅ PDF digital done: %s (%d pages)", file.filename, page_count)
    finally:
        delete_temp_file(file_path)

    job = await ocr_job_service.save(
        db,
        job_type="pdf_digital",
        source_ref=file.filename or "upload.pdf",
        original_filename=file.filename,
        result_md=result_md,
        page_count=page_count,
    )
    return OcrResult.model_validate(job)


@router.post(
    "/scanned",
    summary="Upload PDF scan → Markdown stream (SSE)",
    description=(
        "OCR từng trang PDF scan bằng LightOnOCR-2-1B. "
        "Trả về Server-Sent Events: mỗi trang OCR xong sẽ được gửi ngay về client. "
        "Sau khi stream kết thúc, kết quả được lưu vào DB."
    ),
)
async def upload_scanned_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="File PDF scan (≤ 50MB)"),
    db: DBSession = None,
):
    content = await read_and_validate_upload(file, ALLOWED_PDF_MIME)
    file_path = save_temp_file(content, file.filename or "upload.pdf")
    original_filename = file.filename or "upload.pdf"

    from app.ocr_engine.pipeline import stream_scanned_pdf_pipeline

    # Collect page texts để save DB sau khi stream xong
    collected_pages: list[str] = []

    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            async for sse_event in stream_scanned_pdf_pipeline(file_path):
                yield sse_event

                # Thu thập page text để lưu DB
                try:
                    raw = sse_event.removeprefix("data: ").strip()
                    payload = json.loads(raw)
                    if payload.get("type") == "page":
                        collected_pages.append(payload.get("text", ""))
                except Exception:
                    pass
        finally:
            delete_temp_file(file_path)

        # Lưu DB sau khi stream kết thúc
        if collected_pages:
            from app.ocr_engine.postprocessor import merge_pages
            merged_md = merge_pages(collected_pages)
            background_tasks.add_task(
                _save_job,
                db=db,
                original_filename=original_filename,
                result_md=merged_md,
                page_count=len(collected_pages),
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # Disable nginx buffering
        },
    )


async def _save_job(
    db: DBSession,
    original_filename: str,
    result_md: str,
    page_count: int,
) -> None:
    """Background task: persist the completed OCR job to DB."""
    try:
        job = await ocr_job_service.save(
            db,
            job_type="pdf_scanned",
            source_ref=original_filename,
            original_filename=original_filename,
            result_md=result_md,
            page_count=page_count,
        )
        logger.info("✅ Scanned PDF saved to DB: id=%d (%d pages)", job.id, page_count)
    except Exception:
        logger.exception("❌ Failed to save scanned PDF job to DB")
