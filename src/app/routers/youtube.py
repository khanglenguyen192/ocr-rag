"""
YouTube router — fetch transcript, return OcrResult directly (no DB).
"""
import logging
from fastapi import APIRouter, HTTPException, status

from app.schemas.ocr_job import OcrResult, YoutubeRequest, YoutubeVerifyResponse, YoutubeLanguage
from app.utils.youtube_utils import extract_video_id, format_transcript_to_markdown

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/youtube", tags=["YouTube"])


@router.post(
    "/verify",
    response_model=YoutubeVerifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify YouTube URL & list available transcript languages",
    description="Kiểm tra URL YouTube hợp lệ và trả về danh sách ngôn ngữ transcript có sẵn.",
)
async def verify_youtube_url(body: YoutubeRequest):
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

    video_id = extract_video_id(body.url)
    if not video_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"URL không hợp lệ hoặc không phải YouTube: {body.url}",
        )

    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)

        available_languages: list[YoutubeLanguage] = []
        for t in transcript_list:
            available_languages.append(
                YoutubeLanguage(
                    language=t.language,
                    language_code=t.language_code,
                    is_generated=t.is_generated,
                )
            )

        logger.info("✅ YouTube verify done: video_id=%s, languages=%d", video_id, len(available_languages))
        return YoutubeVerifyResponse(video_id=video_id, available_languages=available_languages)

    except TranscriptsDisabled:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video này đã tắt tính năng phụ đề.")
    except NoTranscriptFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy phụ đề cho video này.")
    except Exception as exc:
        logger.exception("YouTube verify error: %s", exc)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Không thể truy cập YouTube: {exc}")


@router.post(
    "/transcript",
    response_model=OcrResult,
    status_code=status.HTTP_200_OK,
    summary="YouTube URL → Markdown transcript",
    description="Trích xuất phụ đề từ video YouTube và format thành Markdown.",
)
async def get_youtube_transcript(body: YoutubeRequest):
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

    video_id = extract_video_id(body.url)
    if not video_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"URL không hợp lệ hoặc không phải YouTube: {body.url}",
        )

    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=[body.language_code])
        result_md = format_transcript_to_markdown(transcript, video_id)
        logger.info("✅ YouTube transcript done: video_id=%s, lang=%s", video_id, body.language_code)
    except (TranscriptsDisabled, NoTranscriptFound) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy phụ đề: {exc}")

    return OcrResult(
        job_type="youtube",
        original_filename=f"{video_id}.md",
        result_md=result_md,
        page_count=1,
    )
