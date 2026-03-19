"""
YouTube router — fetch transcript, save to PostgreSQL, return OcrResult.
"""
import logging
from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import DBSession
from app.schemas.ocr_job import OcrResult, YoutubeRequest
from app.services.ocr_service import ocr_job_service

from app.utils.youtube_utils import extract_video_id, format_transcript_to_markdown

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/youtube", tags=["YouTube"])


@router.post(
    "/transcript",
    response_model=OcrResult,
    status_code=status.HTTP_200_OK,
    summary="YouTube URL → Markdown transcript",
    description="Trích xuất phụ đề từ video YouTube và format thành Markdown. Kết quả được lưu vào DB.",
)
async def get_youtube_transcript(body: YoutubeRequest, db: DBSession):
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

    video_id = extract_video_id(body.url)
    if not video_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"URL không hợp lệ hoặc không phải YouTube: {body.url}",
        )

    try:
        # youtube-transcript-api v1.0+: dùng instance method fetch()
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(
            video_id,
            languages=["vi", "en", "fr", "de", "ja", "zh", "es", "it"],
        )
        result_md = format_transcript_to_markdown(transcript, video_id)
        logger.info("✅ YouTube transcript done: video_id=%s", video_id)

    except (TranscriptsDisabled, NoTranscriptFound) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy phụ đề cho video này: {exc}",
        )

    job = await ocr_job_service.save(
        db,
        job_type="youtube",
        source_ref=body.url,
        original_filename=f"{video_id}.md",
        result_md=result_md,
        page_count=1,
    )
    return job
