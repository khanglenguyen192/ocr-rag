import os
import uuid
import magic
import logging
from pathlib import Path
from fastapi import UploadFile, HTTPException, status

from app.core.config import settings

logger = logging.getLogger(__name__)

ALLOWED_PDF_MIME = {"application/pdf"}
ALLOWED_IMAGE_MIME = {"image/jpeg", "image/png", "image/bmp", "image/webp", "image/tiff"}
ALLOWED_MIME_ALL = ALLOWED_PDF_MIME | ALLOWED_IMAGE_MIME


async def read_and_validate_upload(
    file: UploadFile,
    allowed_mime: set[str],
) -> bytes:
    """
    Read upload file, validate size and MIME type (magic bytes).
    Returns file bytes.
    """
    content = await file.read()

    # Size check
    if len(content) > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File quá lớn. Tối đa {settings.MAX_FILE_SIZE_MB}MB.",
        )

    # MIME type check via magic bytes
    try:
        mime = magic.from_buffer(content[:2048], mime=True)
    except Exception:
        mime = "application/octet-stream"

    if mime not in allowed_mime:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Định dạng không hỗ trợ: {mime}. Chấp nhận: {', '.join(sorted(allowed_mime))}",
        )

    return content


def save_temp_file(content: bytes, original_filename: str) -> str:
    """Save bytes to a temp file in UPLOAD_DIR. Returns absolute file path."""
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(original_filename).suffix.lower() or ".bin"
    unique_name = f"{uuid.uuid4().hex}{ext}"
    dest = upload_dir / unique_name

    dest.write_bytes(content)
    logger.debug("Saved temp file: %s (%d bytes)", dest, len(content))
    return str(dest)


def delete_temp_file(file_path: str) -> None:
    """Silently remove a temporary file."""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            logger.debug("Deleted temp file: %s", file_path)
    except OSError as e:
        logger.warning("Could not delete temp file %s: %s", file_path, e)

