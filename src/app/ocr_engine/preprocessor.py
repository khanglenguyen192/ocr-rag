"""
Image preprocessor — resize, orientation fix, color normalization.
"""
import gc
import torch
from PIL import Image, ImageOps

from app.core.config import settings


def preprocess_image(image: Image.Image, img_max: int | None = None) -> Image.Image:
    """
    Prepare a PIL image for OCR inference:
    1. Convert to RGB
    2. Fix EXIF orientation
    3. Resize so the longest side ≤ img_max (preserving aspect ratio)
    """
    max_dim = img_max or settings.IMG_MAX

    image = image.convert("RGB")
    image = ImageOps.exif_transpose(image)  # Fix rotation from EXIF metadata

    w, h = image.size
    if max(w, h) > max_dim:
        scale = max_dim / max(w, h)
        new_size = (int(w * scale), int(h * scale))
        image = image.resize(new_size, Image.Resampling.LANCZOS)

    return image


def pdf_to_images(pdf_path: str, dpi: int | None = None) -> list[Image.Image]:
    """
    Render all pages of a PDF to a list of PIL Images.
    Uses pypdfium2 (same engine as the notebook).
    """
    import pypdfium2 as pdfium

    render_dpi = dpi or settings.PDF_DPI
    doc = pdfium.PdfDocument(pdf_path)
    images: list[Image.Image] = []

    try:
        for page in doc:
            bitmap = page.render(scale=render_dpi / 72, rotation=0)
            pil_img = bitmap.to_pil().convert("RGB")
            images.append(pil_img)
    finally:
        doc.close()

    return images


def free_memory(device: str | None = None) -> None:
    """Release unused GPU/MPS memory."""
    dev = device or settings.device
    gc.collect()
    if dev == "cuda":
        torch.cuda.empty_cache()
    elif dev == "mps":
        torch.mps.empty_cache()

