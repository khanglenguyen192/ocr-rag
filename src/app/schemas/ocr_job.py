from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

OcrTaskType = Literal["pdf_digital", "pdf_scanned", "image", "youtube"]


class OcrResult(BaseModel):
    """Response returned directly after OCR processing (with DB record id)."""

    id: int
    job_type: OcrTaskType
    original_filename: str | None = None
    page_count: int = 0
    result_md: str
    created_at: datetime

    model_config = {"from_attributes": True}


class YoutubeRequest(BaseModel):
    """Request body for YouTube transcript endpoint."""

    url: str = Field(..., description="Valid YouTube URL (youtube.com/watch?v=ID or youtu.be/ID)")


class OcrJobSummary(BaseModel):
    """Lightweight record for listing jobs — without result_md content."""

    id: int
    job_type: OcrTaskType
    original_filename: str | None = None
    page_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class PageResponse(BaseModel):
    """Generic paginated response."""

    items: list[OcrJobSummary]
    total: int
    page: int
    size: int
    pages: int
