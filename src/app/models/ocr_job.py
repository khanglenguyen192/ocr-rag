from sqlalchemy import Integer, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.core.database import Base


class OcrJob(Base):
    __tablename__ = "ocr_jobs"
    __table_args__ = {"schema": "pgdbo"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    # Job metadata
    job_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    # pdf_digital | pdf_scanned | image | youtube
    source_ref: Mapped[str] = mapped_column(Text, nullable=False)  # temp path or YouTube URL
    original_filename: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Results
    result_md: Mapped[str | None] = mapped_column(Text, nullable=True)
    page_count: Mapped[int] = mapped_column(Integer, default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"<OcrJob id={self.id} type={self.job_type}>"
