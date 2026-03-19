"""
PDF router — handles both digital PDF and scanned PDF uploads.
Processes synchronously and returns Markdown result directly.
"""
import logging
from fastapi import APIRouter, UploadFile, File, status

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
    response_model=OcrResult,
    status_code=status.HTTP_200_OK,
    summary="Upload PDF scan → Markdown (OCR)",
    description="Chuyển đổi PDF scan (không có text layer) sang Markdown bằng LightOnOCR-2-1B.",
)
async def upload_scanned_pdf(
    file: UploadFile = File(..., description="File PDF scan (≤ 50MB)"),
    db: DBSession = None,
):
    content = await read_and_validate_upload(file, ALLOWED_PDF_MIME)
    file_path = save_temp_file(content, file.filename or "upload.pdf")

    try:
        from app.ocr_engine.pipeline import run_scanned_pdf_pipeline

        result_md, page_count = run_scanned_pdf_pipeline(file_path)
        logger.info("✅ Scanned PDF done: %s (%d pages)", file.filename, page_count)
    finally:
        delete_temp_file(file_path)

    job = await ocr_job_service.save(
        db,
        job_type="pdf_scanned",
        source_ref=file.filename or "upload.pdf",
        original_filename=file.filename,
        result_md=result_md,
        page_count=page_count,
    )
    return OcrResult.model_validate(job)
