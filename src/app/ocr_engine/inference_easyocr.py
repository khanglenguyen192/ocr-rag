"""
EasyOCR inference wrapper.
Singleton reader — loaded once, reused across requests.
"""
import logging
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

_reader = None


def get_easyocr_reader(languages: list[str] | None = None):
    """Return cached EasyOCR reader (load if not yet loaded)."""
    global _reader
    if _reader is not None:
        return _reader

    import easyocr

    langs = languages or ["vi", "en"]
    logger.info("Loading EasyOCR reader, languages=%s", langs)
    _reader = easyocr.Reader(langs, gpu=False)
    logger.info("✅ EasyOCR reader loaded.")
    return _reader


def ocr_image_easyocr(image: Image.Image) -> str:
    """
    Run EasyOCR on a single PIL image.

    Returns:
        Extracted text as plain string (newline-separated).
    """
    reader = get_easyocr_reader()

    # EasyOCR expects numpy array (RGB)
    img_array = np.array(image.convert("RGB"))
    results = reader.readtext(img_array, detail=0, paragraph=True)
    text = "\n".join(results)
    logger.debug("EasyOCR extracted %d chars", len(text))
    return text

