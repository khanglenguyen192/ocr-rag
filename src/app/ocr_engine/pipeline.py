"""
OCR pipeline — orchestrates preprocessor → inference → postprocessor.
Called by Celery workers.
"""
import asyncio
import json
import logging
from collections.abc import AsyncGenerator
from PIL import Image

from app.ocr_engine.preprocessor import pdf_to_images, preprocess_image, free_memory
from app.ocr_engine.inference import ocr_image
from app.ocr_engine.postprocessor import merge_pages, clean_markdown

logger = logging.getLogger(__name__)


def _sse(payload: dict) -> str:
    """Format a dict as an SSE data line."""
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


def run_image_pipeline(file_path: str) -> tuple[str, int]:
    """
    OCR a single image file.

    Returns:
        (markdown_text, page_count=1)
    """
    logger.info("Running image OCR pipeline: %s", file_path)
    img = Image.open(file_path).convert("RGB")
    text = ocr_image(img)
    return clean_markdown(text), 1


def run_scanned_pdf_pipeline(file_path: str) -> tuple[str, int]:
    """
    OCR a scanned PDF: render each page → OCR → merge.

    Returns:
        (merged_markdown, page_count)
    """
    logger.info("Running scanned PDF OCR pipeline: %s", file_path)
    images = pdf_to_images(file_path)
    total = len(images)
    logger.info("Rendered %d pages from PDF", total)

    page_texts: list[str] = []
    for i, img in enumerate(images):
        logger.info("  OCR page %d/%d (%dx%d)...", i + 1, total, img.size[0], img.size[1])
        text = ocr_image(img)
        page_texts.append(text)

        del img
        images[i] = None  # type: ignore[assignment]
        free_memory()

    merged = merge_pages(page_texts)
    return clean_markdown(merged), total


async def stream_scanned_pdf_pipeline(file_path: str) -> AsyncGenerator[str, None]:
    """
    Async generator: OCR mỗi trang trong thread riêng rồi yield SSE event ngay,
    event loop không bị block → client nhận được từng trang khi OCR xong.

    SSE events:
        data: {"type": "start",  "total": N}
        data: {"type": "page",   "page": i, "total": N, "text": "..."}
        data: {"type": "done",   "page_count": N}
        data: {"type": "error",  "message": "..."}
    """
    # --- Bước 1: render PDF → images (chạy trong thread) ---
    logger.info("Streaming scanned PDF OCR pipeline: %s", file_path)
    try:
        images: list[Image.Image] = await asyncio.to_thread(pdf_to_images, file_path)
    except Exception as exc:
        logger.exception("Failed to render PDF pages: %s", exc)
        yield _sse({"type": "error", "message": str(exc)})
        return

    total = len(images)
    logger.info("Rendered %d pages from PDF (streaming)", total)
    yield _sse({"type": "start", "total": total})

    # --- Bước 2: OCR từng trang, mỗi trang chạy trong thread riêng ---
    for i in range(total):
        img = images[i]
        page_num = i + 1
        logger.info("  OCR page %d/%d (%dx%d)...", page_num, total, img.size[0], img.size[1])
        try:
            # Chạy blocking inference trong thread pool → không block event loop
            text: str = await asyncio.to_thread(ocr_image, img)
            cleaned = clean_markdown(text)
            yield _sse({"type": "page", "page": page_num, "total": total, "text": cleaned})
        except Exception as exc:
            logger.exception("Error OCR page %d: %s", page_num, exc)
            yield _sse({"type": "error", "message": f"Page {page_num}: {exc}"})
        finally:
            del img
            images[i] = None  # type: ignore[assignment]
            await asyncio.to_thread(free_memory)

    yield _sse({"type": "done", "page_count": total})


def run_digital_pdf_pipeline(file_path: str) -> tuple[str, int]:
    """
    Convert a digital (text-layer) PDF to Markdown using pymupdf4llm.

    Returns:
        (markdown_text, page_count)
    """
    import pymupdf4llm
    import fitz  # PyMuPDF

    logger.info("Running digital PDF pipeline (pymupdf4llm): %s", file_path)

    doc = fitz.open(file_path)
    page_count = len(doc)
    doc.close()

    md_text = pymupdf4llm.to_markdown(file_path)
    return clean_markdown(md_text), page_count


