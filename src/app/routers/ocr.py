"""
OCR router — image file upload.
Processes synchronously, returns OcrResult directly (no DB).
"""
import logging
from fastapi import APIRouter, UploadFile, File, Query, status

from app.ocr_engine.pipeline import OcrEngine
from app.schemas.ocr_job import OcrResult
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
    description="Nhận diện văn bản từ ảnh. Hỗ trợ 3 engine: lighton, easyocr, paddleocr.",
)
async def upload_image_for_ocr(
    file: UploadFile = File(..., description="File ảnh (≤ 50MB)"),
    engine: OcrEngine = Query("lighton", description="OCR engine: lighton | easyocr | paddleocr"),
):
    content = await read_and_validate_upload(file, ALLOWED_IMAGE_MIME)
    file_path = save_temp_file(content, file.filename or "upload.jpg")

    try:
        from app.ocr_engine.pipeline import run_image_pipeline

        result_md, page_count = run_image_pipeline(file_path, engine=engine)
        logger.info("✅ Image OCR done [engine=%s]: %s", engine, file.filename)
    finally:
        delete_temp_file(file_path)

    return OcrResult(
        job_type="image",
        original_filename=file.filename,
        result_md=result_md,
        page_count=page_count,
    )
