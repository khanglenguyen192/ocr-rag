"""
Tests for OCR endpoints — no DB, no Celery, synchronous processing mocked.
"""
import pytest
from unittest.mock import patch
from httpx import AsyncClient
from io import BytesIO


def _make_pdf_bytes() -> bytes:
    return b"%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\nxref\n0 1\n0000000000 65535 f\ntrailer<</Size 1>>\nstartxref\n9\n%%EOF"


@pytest.mark.asyncio
async def test_upload_digital_pdf_returns_result(client: AsyncClient):
    pdf_bytes = _make_pdf_bytes()

    with patch("app.routers.pdf.run_digital_pdf_pipeline", return_value=("# Hello PDF", 2)):
        response = await client.post(
            "/api/v1/pdf/digital",
            files={"file": ("test.pdf", BytesIO(pdf_bytes), "application/pdf")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["job_type"] == "pdf_digital"
    assert data["result_md"] == "# Hello PDF"
    assert data["page_count"] == 2
    assert data["original_filename"] == "test.pdf"


@pytest.mark.asyncio
async def test_upload_scanned_pdf_returns_result(client: AsyncClient):
    pdf_bytes = _make_pdf_bytes()

    with patch("app.routers.pdf.run_scanned_pdf_pipeline", return_value=("# Scanned", 1)):
        response = await client.post(
            "/api/v1/pdf/scanned",
            files={"file": ("scan.pdf", BytesIO(pdf_bytes), "application/pdf")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["job_type"] == "pdf_scanned"
    assert data["result_md"] == "# Scanned"


@pytest.mark.asyncio
async def test_upload_image_returns_result(client: AsyncClient):
    jpeg_bytes = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xd9"

    with patch("app.routers.ocr.run_image_pipeline", return_value=("## Image OCR", 1)):
        response = await client.post(
            "/api/v1/ocr/image",
            files={"file": ("photo.jpg", BytesIO(jpeg_bytes), "image/jpeg")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["job_type"] == "image"
    assert data["result_md"] == "## Image OCR"


@pytest.mark.asyncio
async def test_youtube_invalid_url(client: AsyncClient):
    response = await client.post(
        "/api/v1/youtube/transcript",
        json={"url": "https://example.com/not-youtube"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_youtube_valid_url(client: AsyncClient):
    mock_transcript = [type("T", (), {"start": 0.0, "text": "Hello world"})()]

    with patch("app.routers.youtube.YouTubeTranscriptApi") as mock_api:
        mock_api.return_value.fetch.return_value = mock_transcript
        response = await client.post(
            "/api/v1/youtube/transcript",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["job_type"] == "youtube"
    assert "result_md" in data


@pytest.mark.asyncio
async def test_download_endpoint(client: AsyncClient):
    response = await client.post(
        "/api/v1/download",
        json={"result_md": "# Hello", "filename": "output.md"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/markdown")
    assert "attachment" in response.headers["content-disposition"]
    assert response.content == b"# Hello"
