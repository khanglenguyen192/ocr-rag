"""
OCR pipeline — orchestrates preprocessor → inference → postprocessor.
Called by Celery workers.
"""
import logging
from PIL import Image

from app.ocr_engine.preprocessor import pdf_to_images, preprocess_image, free_memory
from app.ocr_engine.inference import ocr_image
from app.ocr_engine.postprocessor import merge_pages, clean_markdown

logger = logging.getLogger(__name__)


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

        # Release memory after each page
        del img
        images[i] = None  # type: ignore[assignment]
        free_memory()

    merged = merge_pages(page_texts)
    return clean_markdown(merged), total


def run_digital_pdf_pipeline(file_path: str) -> tuple[str, int]:
    """
    Convert a digital (text-layer) PDF to Markdown using pymupdf4llm.

    Returns:
        (markdown_text, page_count)
    """
    import pymupdf4llm
    import fitz  # PyMuPDF

    logger.info("Running digital PDF pipeline (pymupdf4llm): %s", file_path)

    # Get page count
    doc = fitz.open(file_path)
    page_count = len(doc)
    doc.close()

    md_text = pymupdf4llm.to_markdown(file_path)
    return clean_markdown(md_text), page_count

