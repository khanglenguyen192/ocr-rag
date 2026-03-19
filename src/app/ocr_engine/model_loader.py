"""
Model loader — singleton pattern for LightOnOCR-2-1B.
Loaded once at worker startup, reused across all tasks.
"""
import logging
from functools import lru_cache

import torch
from transformers import LightOnOcrForConditionalGeneration, LightOnOcrProcessor

from app.core.config import settings

logger = logging.getLogger(__name__)

# Module-level cache (set on first call)
_model = None
_processor = None


def load_model() -> tuple:
    """
    Load LightOnOCR model and processor.
    Called once — subsequent calls return cached instances.
    """
    global _model, _processor

    if _model is not None and _processor is not None:
        return _model, _processor

    logger.info(
        "Loading LightOnOCR-2-1B from '%s' on device=%s dtype=%s",
        settings.MODEL_DIR,
        settings.device,
        settings.dtype,
    )

    _processor = LightOnOcrProcessor.from_pretrained(
        settings.MODEL_DIR, trust_remote_code=True
    )
    _model = LightOnOcrForConditionalGeneration.from_pretrained(
        settings.MODEL_DIR,
        torch_dtype=settings.dtype,
        trust_remote_code=True,
    ).to(settings.device)
    _model.eval()

    logger.info("✅ LightOnOCR-2-1B loaded successfully.")
    return _model, _processor


def get_model():
    """Return cached model (load if not yet loaded)."""
    model, _ = load_model()
    return model


def get_processor():
    """Return cached processor (load if not yet loaded)."""
    _, processor = load_model()
    return processor

