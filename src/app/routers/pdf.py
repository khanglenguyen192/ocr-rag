"""
PDF router — handles both digital PDF and scanned PDF uploads.
- Digital PDF: synchronous, returns JSON OcrResult directly (no DB).
- Scanned PDF: streams SSE events per page.
"""
import json
import logging
from collections.abc import AsyncGenerator

from fastapi import APIRouter, UploadFile, File, Query, status
from fastapi.responses import StreamingResponse

from app.ocr_engine.pipeline import OcrEngine
from app.schemas.ocr_job import OcrResult
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
):
    content = await read_and_validate_upload(file, ALLOWED_PDF_MIME)
    file_path = save_temp_file(content, file.filename or "upload.pdf")

    try:
        from app.ocr_engine.pipeline import run_digital_pdf_pipeline

        result_md, page_count = run_digital_pdf_pipeline(file_path)
        logger.info("✅ PDF digital done: %s (%d pages)", file.filename, page_count)
    finally:
        delete_temp_file(file_path)

    return OcrResult(
        job_type="pdf_digital",
        original_filename=file.filename,
        result_md=result_md,
        page_count=page_count,
    )


@router.post(
    "/scanned",
    summary="Upload PDF scan → Markdown stream (SSE)",
    description=(
        "OCR từng trang PDF scan. Hỗ trợ 3 engine: lighton, easyocr, paddleocr. "
        "Trả về Server-Sent Events: mỗi trang OCR xong sẽ được gửi ngay về client."
    ),
)
async def upload_scanned_pdf(
    file: UploadFile = File(..., description="File PDF scan (≤ 50MB)"),
    engine: OcrEngine = Query("lighton", description="OCR engine: lighton | easyocr | paddleocr"),
):
    content = await read_and_validate_upload(file, ALLOWED_PDF_MIME)
    file_path = save_temp_file(content, file.filename or "upload.pdf")

    from app.ocr_engine.pipeline import stream_scanned_pdf_pipeline

    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            async for sse_event in stream_scanned_pdf_pipeline(file_path, engine=engine):
                yield sse_event
        finally:
            delete_temp_file(file_path)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
