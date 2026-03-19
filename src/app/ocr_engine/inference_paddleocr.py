"""
PaddleOCR inference wrapper — compatible with PaddleOCR v3+.
Singleton instance — loaded once, reused across requests.
  Install: pip install paddlepaddle paddleocr
"""
import logging
import os
import numpy as np
from PIL import Image

# Tắt connectivity check khi start (tăng tốc khởi động)
os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")

logger = logging.getLogger(__name__)

_ocr = None


def get_paddle_ocr():
    """Return cached PaddleOCR instance (load if not yet loaded)."""
    global _ocr
    if _ocr is not None:
        return _ocr

    try:
        from paddleocr import PaddleOCR
    except ImportError as exc:
        raise RuntimeError(
            "paddleocr chưa được cài. Chạy: pip install paddlepaddle paddleocr"
        ) from exc

    logger.info("Loading PaddleOCR v3+ (lang=ch, use_textline_orientation=True)...")
    # PaddleOCR v3: bỏ use_gpu / show_log / use_angle_cls
    # dùng use_textline_orientation thay cho use_angle_cls
    _ocr = PaddleOCR(
        lang="ch",                       # "ch" hỗ trợ tiếng Việt tốt hơn "vi" trong v3
        use_textline_orientation=True,   # tự xoay dòng chữ nghiêng (thay use_angle_cls)
    )
    logger.info("✅ PaddleOCR loaded.")
    return _ocr


def ocr_image_paddle(image: Image.Image) -> str:
    """
    Run PaddleOCR v3 on a single PIL image.

    Returns:
        Extracted text as plain string (newline-separated by line).
    """
    ocr = get_paddle_ocr()
    img_array = np.array(image.convert("RGB"))
    results = ocr.ocr(img_array)

    lines: list[str] = []
    if results:
        for res in results:
            # v3: result item là dict-like với key rec_texts (list[str])
            texts = res.get("rec_texts") if hasattr(res, "get") else None
            if texts:
                lines.extend(texts)

    text = "\n".join(lines)
    logger.debug("PaddleOCR extracted %d chars", len(text))
    return text

