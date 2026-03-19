"""
Core OCR inference — wraps LightOnOCR-2-1B model.generate().
Mirrors the notebook logic but as a clean module.
"""
import logging
import torch
from PIL import Image

from app.core.config import settings
from app.ocr_engine.model_loader import get_model, get_processor
from app.ocr_engine.preprocessor import preprocess_image, free_memory

logger = logging.getLogger(__name__)

# Task-specific prompt strategies
TASK_PROMPTS: dict[str, list[dict]] = {
    "markdown": [
        {
            "role": "user",
            "content": [{"type": "image", "url": None}],
        }
    ],
    "plain_text": [
        {
            "role": "user",
            "content": [{"type": "image", "url": None}],
        }
    ],
    "handwriting": [
        {
            "role": "user",
            "content": [{"type": "image", "url": None}],
        }
    ],
}


def ocr_image(
    image: Image.Image,
    task: str = "markdown",
    max_tokens: int | None = None,
) -> str:
    """
    Run OCR inference on a single PIL image.

    Args:
        image: PIL Image (will be converted to RGB and resized internally)
        task: "markdown" | "plain_text" | "handwriting"
        max_tokens: Override MAX_TOKENS from settings

    Returns:
        Extracted text / Markdown string
    """
    model = get_model()
    processor = get_processor()
    device = settings.device
    dtype = settings.dtype
    tokens = max_tokens or settings.MAX_TOKENS

    img = preprocess_image(image)

    conversation = [
        {
            "role": "user",
            "content": [{"type": "image", "url": img}],
        }
    ]

    try:
        inputs = processor.apply_chat_template(
            conversation,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        )

        # Move tensors to correct device/dtype
        inputs = {
            k: v.to(device=device, dtype=dtype) if v.is_floating_point() else v.to(device)
            for k, v in inputs.items()
        }

        with torch.inference_mode():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=tokens,
                do_sample=False,
            )

        input_len = inputs["input_ids"].shape[1]
        generated_ids = output_ids[0, input_len:]
        result = processor.decode(generated_ids, skip_special_tokens=True)

        del inputs, output_ids, generated_ids
        free_memory(device)

        return result.strip()

    except Exception as e:
        logger.exception("OCR inference failed: %s", e)
        free_memory(device)
        raise

