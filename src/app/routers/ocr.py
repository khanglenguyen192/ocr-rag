"""
OCR router — image file upload.
Processes synchronously, saves result to PostgreSQL, returns full OcrResult.
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
    ALLOWED_IMAGE_MIME,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ocr", tags=["OCR Image"])


@router.post(
    "/image",
    response_model=OcrResult,
    status_code=status.HTTP_200_OK,
    summary="Upload ảnh → Markdown (OCR)",
    description="Nhận diện văn bản từ ảnh bằng LightOnOCR-2-1B. Kết quả được lưu vào DB.",
)
async def upload_image_for_ocr(
    db: DBSession,
    file: UploadFile = File(..., description="File ảnh (≤ 50MB)"),
):
    content = await read_and_validate_upload(file, ALLOWED_IMAGE_MIME)
    file_path = save_temp_file(content, file.filename or "upload.jpg")

    try:
        from app.ocr_engine.pipeline import run_image_pipeline

        result_md, page_count = run_image_pipeline(file_path)
        logger.info("✅ Image OCR done: %s", file.filename)
    finally:
        delete_temp_file(file_path)

    job = await ocr_job_service.save(
        db,
        job_type="image",
        source_ref=file.filename or "upload.jpg",
        original_filename=file.filename,
        result_md=result_md,
        page_count=page_count,
    )
    return job
