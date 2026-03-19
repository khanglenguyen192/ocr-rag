"""
OcrJobService — DB CRUD for OCR jobs (PostgreSQL via SQLAlchemy async).
"""
import logging
import math
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ocr_job import OcrJob
from app.schemas.ocr_job import OcrJobSummary, PageResponse

logger = logging.getLogger(__name__)


class OcrJobService:

    async def save(
        self,
        db: AsyncSession,
        *,
        job_type: str,
        source_ref: str,
        original_filename: str | None,
        result_md: str,
        page_count: int,
    ) -> OcrJob:
        """Persist a completed OCR result to DB."""
        job = OcrJob(
            job_type=job_type,
            source_ref=source_ref,
            original_filename=original_filename,
            result_md=result_md,
            page_count=page_count,
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        logger.info("Saved OcrJob id=%d type=%s", job.id, job.job_type)
        return job

    async def get(self, db: AsyncSession, job_id: int) -> OcrJob | None:
        result = await db.execute(select(OcrJob).where(OcrJob.id == job_id))
        return result.scalar_one_or_none()

    async def list_jobs(
        self, db: AsyncSession, page: int = 1, size: int = 20
    ) -> PageResponse:
        offset = (page - 1) * size

        total = (await db.execute(select(func.count()).select_from(OcrJob))).scalar_one()
        rows = (
            await db.execute(
                select(OcrJob).order_by(OcrJob.created_at.desc()).offset(offset).limit(size)
            )
        ).scalars().all()

        return PageResponse(
            items=[OcrJobSummary.model_validate(r) for r in rows],
            total=total,
            page=page,
            size=size,
            pages=math.ceil(total / size) if total > 0 else 0,
        )


ocr_job_service = OcrJobService()
