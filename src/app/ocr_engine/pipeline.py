"""
OCR pipeline — orchestrates preprocessor → inference → postprocessor.
Called by Celery workers.
"""
import asyncio
import json
import logging
import time
from collections.abc import AsyncGenerator
from functools import wraps
from typing import Literal
from PIL import Image

from app.ocr_engine.preprocessor import pdf_to_images, preprocess_image, free_memory
from app.ocr_engine.inference import ocr_image
from app.ocr_engine.postprocessor import merge_pages, clean_markdown

logger = logging.getLogger(__name__)

# Supported OCR engine identifiers
OcrEngine = Literal["lighton", "easyocr", "paddleocr"]


def _timed(fn):
    """Decorator: log execution time of sync functions."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = (time.perf_counter() - t0) * 1000
        logger.info("⏱ %s finished in %.0f ms", fn.__name__, elapsed)
        return result
    return wrapper


def _run_ocr(image: Image.Image, engine: OcrEngine = "lighton") -> str:
    """Dispatch OCR to the selected engine."""
    if engine == "easyocr":
        from app.ocr_engine.inference_easyocr import ocr_image_easyocr
        return ocr_image_easyocr(image)
    elif engine == "paddleocr":
        from app.ocr_engine.inference_paddleocr import ocr_image_paddle
        return ocr_image_paddle(image)
    else:  # default: lighton
        return ocr_image(image)


def _sse(payload: dict) -> str:
    """Format a dict as an SSE data line."""
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


@_timed
def run_image_pipeline(file_path: str, engine: OcrEngine = "lighton") -> tuple[str, int]:
    """
    OCR a single image file.

    Returns:
        (markdown_text, page_count=1)
    """
    logger.info("Running image OCR pipeline [engine=%s]: %s", engine, file_path)
    img = Image.open(file_path).convert("RGB")
    text = _run_ocr(img, engine)
    return clean_markdown(text), 1


@_timed
def run_scanned_pdf_pipeline(file_path: str, engine: OcrEngine = "lighton") -> tuple[str, int]:
    """
    OCR a scanned PDF: render each page → OCR → merge.

    Returns:
        (merged_markdown, page_count)
    """
    logger.info("Running scanned PDF OCR pipeline [engine=%s]: %s", engine, file_path)
    images = pdf_to_images(file_path)
    total = len(images)
    logger.info("Rendered %d pages from PDF", total)

    page_texts: list[str] = []
    for i, img in enumerate(images):
        logger.info("  OCR page %d/%d (%dx%d)...", i + 1, total, img.size[0], img.size[1])
        text = _run_ocr(img, engine)
        page_texts.append(text)

        del img
        images[i] = None  # type: ignore[assignment]
        free_memory()

    merged = merge_pages(page_texts)
    return clean_markdown(merged), total


async def stream_scanned_pdf_pipeline(
    file_path: str,
    engine: OcrEngine = "lighton",
) -> AsyncGenerator[str, None]:
    """
    Async generator: OCR mỗi trang trong thread riêng rồi yield SSE event ngay.

    SSE events:
        data: {"type": "start",   "total": N}
        data: {"type": "page",    "page": i, "total": N, "text": "...", "page_elapsed_ms": X}
        data: {"type": "done",    "page_count": N, "elapsed_ms": X}
        data: {"type": "error",   "message": "..."}
    """
    logger.info("Streaming scanned PDF OCR pipeline [engine=%s]: %s", engine, file_path)
    pipeline_start = time.perf_counter()

    try:
        images: list[Image.Image] = await asyncio.to_thread(pdf_to_images, file_path)
    except Exception as exc:
        logger.exception("Failed to render PDF pages: %s", exc)
        yield _sse({"type": "error", "message": str(exc)})
        return

    total = len(images)
    logger.info("Rendered %d pages from PDF (streaming)", total)
    yield _sse({"type": "start", "total": total})

    for i in range(total):
        img = images[i]
        page_num = i + 1
        logger.info("  OCR page %d/%d (%dx%d)...", page_num, total, img.size[0], img.size[1])
        page_start = time.perf_counter()
        try:
            text: str = await asyncio.to_thread(_run_ocr, img, engine)
            cleaned = clean_markdown(text)
            page_elapsed = round((time.perf_counter() - page_start) * 1000)
            logger.info("  ⏱ Page %d OCR done in %d ms", page_num, page_elapsed)
            yield _sse({"type": "page", "page": page_num, "total": total, "text": cleaned, "page_elapsed_ms": page_elapsed})
        except Exception as exc:
            logger.exception("Error OCR page %d: %s", page_num, exc)
            yield _sse({"type": "error", "message": f"Page {page_num}: {exc}"})
        finally:
            del img
            images[i] = None  # type: ignore[assignment]
            await asyncio.to_thread(free_memory)

    total_elapsed = round((time.perf_counter() - pipeline_start) * 1000)
    logger.info("⏱ stream_scanned_pdf_pipeline total: %d ms", total_elapsed)
    yield _sse({"type": "done", "page_count": total, "elapsed_ms": total_elapsed})


@_timed
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

