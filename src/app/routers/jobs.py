"""
Download router — stream Markdown result as a .md file.
No DB needed: client sends back the result_md string to download.
"""
import io
import logging
from pathlib import Path

from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/download", tags=["Download"])


class DownloadRequest(BaseModel):
    result_md: str
    filename: str = "result.md"


@router.post(
    "",
    summary="Tải xuống kết quả Markdown",
    description="Nhận result_md từ client và stream về dưới dạng file .md.",
    status_code=status.HTTP_200_OK,
)
async def download_markdown(body: DownloadRequest):
    stem = Path(body.filename).stem
    filename = f"{stem}.md" if not body.filename.endswith(".md") else body.filename

    content_bytes = body.result_md.encode("utf-8")

    return StreamingResponse(
        io.BytesIO(content_bytes),
        media_type="text/markdown; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(len(content_bytes)),
        },
    )
