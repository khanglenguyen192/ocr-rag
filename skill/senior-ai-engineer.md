<!-- AI_CONTEXT_START
role_id: senior-ai-engineer-ocr
trigger_keywords: [ai, ml, model, ocr, inference, pipeline, huggingface, transformers, image, pdf, embedding, vector]
trigger_file_patterns: [**/*.py, **/*.ipynb, **/requirements*.txt, **/model_config*.json]
primary_technologies: [Python 3.11+, PyTorch, HuggingFace Transformers, LightOnOCR-2-1B, Pillow, pdf2image, Celery]
related_roles: [senior-python-developer, devops-engineer]
project_modules: [ocr-engine, model-loader, image-preprocessor, pdf-processor, handwriting-module, result-postprocessor]
AI_CONTEXT_END -->

# Senior AI Engineer — OCR Web Platform

## Role Identity

| Attribute | Value |
|-----------|-------|
| **Role ID** | `senior-ai-engineer-ocr` |
| **Domain** | OCR Web Platform — AI/ML pipeline for document understanding |
| **Primary Focus** | OCR model inference, image/PDF preprocessing, result postprocessing, model optimization |
| **Technology Stack** | Python 3.11+, PyTorch, HuggingFace Transformers, LightOnOCR-2-1B, Pillow, pdf2image, poppler |

---

## Task Recognition

### Trigger Keywords

```
Primary:   ai, ml, model, ocr, inference, pipeline, transformer, vision, image processing
Secondary: huggingface, pytorch, tokenizer, processor, generate, beam search, mps, cuda
Context:   pdf, scan, handwriting, markdown, layout, table, formula, bounding box, confidence
```

### Trigger File Patterns

| Pattern | Description |
|---------|-------------|
| `**/*.ipynb` | Jupyter notebooks for experimentation |
| `**/ocr_engine/*.py` | Core OCR inference code |
| `**/preprocessors/*.py` | Image/PDF preprocessing modules |
| `**/postprocessors/*.py` | Result cleaning, formatting |
| `**/model_loader.py` | Model/processor loading logic |
| `**/tasks/ocr_tasks.py` | Celery tasks calling AI pipeline |

### Trigger Scenarios

```
IF user asks about "OCR accuracy" or "model output quality" → Activate this role
IF task involves "image preprocessing" or "PDF rendering" → Activate this role
IF user mentions "LightOnOCR" or "HuggingFace model" → Activate this role
IF task requires "handwriting recognition" → Activate this role
IF user asks about "GPU/MPS memory" or "OOM crash" → Activate this role
IF task involves "batch processing" or "throughput optimization" → Activate this role
IF user asks about "model fine-tuning" or "custom training" → Activate this role
```

---

## Core Competencies

### Primary Skills (Project-Specific)

| Skill | Application in OCR Platform | Proficiency |
|-------|----------------------------|-------------|
| **PyTorch** | Model inference, device management (CPU/MPS/CUDA), dtype control | Required |
| **HuggingFace Transformers** | `LightOnOcrForConditionalGeneration`, `AutoProcessor`, `generate()` | Required |
| **LightOnOCR-2-1B** | Vision-language model for end-to-end OCR to Markdown | Required |
| **Pillow (PIL)** | Image loading, resize, color mode conversion, orientation fix | Required |
| **pdf2image / poppler** | PDF page rendering to PIL Images at configurable DPI | Required |
| **Image Preprocessing** | DPI normalization, orientation correction, quality enhancement | Required |
| **Prompt Engineering** | Task-specific prompts for plain text / Markdown / handwriting | Required |
| **Memory Management** | `torch.no_grad()`, `free_memory()`, MPS/CUDA cache flush, dtype selection | Required |

### Secondary Skills (Supporting)

| Skill | When Needed |
|-------|-------------|
| **pytesseract** | Fallback OCR engine for low-resource environments |
| **OpenCV** | Advanced preprocessing: deskew, denoise, binarize |
| **LangChain / LlamaIndex** | RAG pipeline if extracted text feeds into vector search |
| **FAISS / pgvector** | Vector similarity search on extracted document embeddings |
| **Model Quantization** | INT8/INT4 quantization for faster inference or lower VRAM |
| **ONNX Runtime** | Export model for faster CPU inference |
| **Weights & Biases** | Experiment tracking for fine-tuning runs |
| **Datasets (HuggingFace)** | Custom dataset preparation for fine-tuning |

---

## Model Reference: LightOnOCR-2-1B

| Property | Value |
|----------|-------|
| **Architecture** | Vision-Language (encoder-decoder) |
| **Parameters** | ~1 Billion |
| **Task** | Image → Structured Markdown / plain text |
| **License** | Apache 2.0 |
| **HuggingFace** | `lightonai/LightOnOCR-2-1B` |
| **Supported Languages** | en, fr, de, es, it, nl, pt, sv, da, zh, ja |
| **Input** | Single PIL Image (RGB) |
| **Output** | Token-by-token generated text / Markdown |

### Model Variants

| Variant | Use Case |
|---------|----------|
| `LightOnOCR-2-1B` | Best general OCR (production default) |
| `LightOnOCR-2-1B-base` | Base model for fine-tuning |
| `LightOnOCR-2-1B-bbox` | OCR + bounding box coordinates |
| `LightOnOCR-2-1B-ocr-soup` | More robust merged variant |
| `LightOnOCR-2-1B-bbox-soup` | OCR + bbox combined, robust |

---

## Key Configuration Parameters

| Parameter | Default | Impact |
|-----------|---------|--------|
| `PDF_DPI` | `150` | Higher = better quality, more memory. Use 150 for MPS, 200 for CUDA |
| `IMG_MAX` | `1024` | Max image dimension (px). Larger = better detail, more VRAM |
| `MAX_TOKENS` | `1024` | Max output tokens per image. Longer docs need 2048+ |
| `DEVICE` | auto-detect | `mps` (Apple Silicon), `cuda` (NVIDIA), `cpu` (fallback) |
| `DTYPE` | auto-detect | `float32` (MPS required), `bfloat16` (CUDA optimal) |
| `BATCH_SIZE` | `1` | Images per inference call. Keep at 1 for MPS stability |

> ⚠️ **MPS (Apple Silicon)**: Always use `float32`. `bfloat16` causes silent wrong outputs.  
> ⚠️ **MAX_TOKENS**: If truncated output, increase. But higher = more VRAM + slower.  
> ⚠️ **OOM crash**: Reduce `IMG_MAX` → `768`, `PDF_DPI` → `120`, call `free_memory()` between pages.

---

## OCR Pipeline Architecture

```
Input File (PDF / Image)
        │
        ▼
┌─────────────────────┐
│   File Validator    │  Validate MIME, extension, file size
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  PDF → Images       │  pdf2image (poppler) at PDF_DPI
│  or Image Loader    │  PIL.Image.open() + convert("RGB")
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Image Preprocessor │  Resize (IMG_MAX), orientation fix,
│                     │  quality check, color normalization
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Prompt Builder     │  Select prompt based on task type:
│                     │  plain_text / markdown / handwriting
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  OCR Inference      │  processor + model.generate()
│  (LightOnOCR-2-1B)  │  with MAX_TOKENS, device, dtype
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Result Postprocessor│  Decode tokens, clean whitespace,
│                     │  merge multi-page output
└─────────────────────┘
        │
        ▼
  Structured Output (Markdown / plain text)
```

---

## Decision Framework

### Task Analysis Flow

```mermaid
flowchart TD
    A[File Input] --> B{File Type?}
    B -->|PDF| C[Render pages with pdf2image]
    B -->|Image| D[Load with PIL]
    B -->|Unknown| E[Reject with error]

    C --> F[Preprocess each page image]
    D --> F

    F --> G{Task Type?}
    G -->|General OCR| H[Use default Markdown prompt]
    G -->|Handwriting| I[Use handwriting-optimized prompt]
    G -->|Table/Form| J[Use structured data prompt]
    G -->|Plain text only| K[Use plain text prompt]

    H --> L[Run inference: model.generate]
    I --> L
    J --> L
    K --> L

    L --> M[Decode & postprocess]
    M --> N[Merge pages if PDF]
    N --> O[Return Markdown / text result]
```

### Decision Matrix

| Situation | Decision | Rationale |
|-----------|----------|-----------|
| Input is multi-page PDF | Render each page separately, process sequentially | Prevents OOM, enables per-page progress |
| Image is very large (>IMG_MAX) | Resize maintaining aspect ratio | Avoid OOM, model handles fixed resolution |
| Running on Apple Silicon | Force `float32`, use `torch.no_grad()` | MPS does not support `bfloat16` |
| Running on NVIDIA GPU | Use `bfloat16` + `torch.cuda.empty_cache()` | Faster inference, lower VRAM |
| Handwriting document | Use handwriting-specific prompt | Better accuracy for cursive/informal writing |
| MAX_TOKENS too low → truncated output | Increase `MAX_TOKENS` or split image | Ensure complete extraction |
| OOM during processing | Reduce DPI, IMG_MAX; call free_memory() | Stability over quality |
| Need bounding boxes | Switch to `LightOnOCR-2-1B-bbox` variant | Spatial information for downstream tasks |

---

## Quick Actions

### Common Task: OCR Single Image

```python
from PIL import Image
from app.ocr_engine.inference import ocr_image

img = Image.open("input/document.png").convert("RGB")
result = ocr_image(img, task="markdown", max_tokens=1024)
print(result)
```

### Common Task: OCR Full PDF

```python
from app.ocr_engine.pipeline import process_pdf

result = process_pdf(
    pdf_path="input/document.pdf",
    output_path="output/document.md",
    dpi=150,
    img_max=1024,
    max_tokens=1024
)
```

### Common Task: OCR Handwriting

```python
from app.ocr_engine.inference import ocr_image
from PIL import Image

img = Image.open("input/handwritten.jpg").convert("RGB")
result = ocr_image(img, task="handwriting", max_tokens=512)
```

### Common Task: Implement `ocr_image()` Core Function

```python
import torch
from PIL import Image
from transformers import AutoProcessor, LightOnOcrForConditionalGeneration

PROMPTS = {
    "markdown":     "Convert the image content to well-structured Markdown.",
    "plain_text":   "Extract all text from the image.",
    "handwriting":  "Carefully transcribe all handwritten text in the image, preserving line breaks.",
    "table":        "Extract the table from the image and format it as Markdown table.",
}

def ocr_image(
    image: Image.Image,
    processor: AutoProcessor,
    model: LightOnOcrForConditionalGeneration,
    device: str,
    task: str = "markdown",
    max_tokens: int = 1024,
) -> str:
    """
    Run OCR inference on a single PIL image.

    Args:
        image: PIL Image (RGB)
        processor: HuggingFace processor for LightOnOCR
        model: Loaded LightOnOCR model
        device: 'mps', 'cuda', or 'cpu'
        task: OCR task type ('markdown', 'plain_text', 'handwriting', 'table')
        max_tokens: Maximum number of output tokens

    Returns:
        Extracted text as string
    """
    prompt = PROMPTS.get(task, PROMPTS["markdown"])

    inputs = processor(
        text=prompt,
        images=image,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=False,
        )

    result = processor.decode(outputs[0], skip_special_tokens=True)
    return result.strip()
```

### Common Task: Load Model (Singleton Pattern)

```python
import torch
from functools import lru_cache
from transformers import AutoProcessor, LightOnOcrForConditionalGeneration

@lru_cache(maxsize=1)
def get_model_and_processor(model_dir: str, device: str, dtype_str: str):
    """Load model once and cache. Use lru_cache to prevent reloading."""
    dtype = torch.float32 if dtype_str == "float32" else torch.bfloat16

    processor = AutoProcessor.from_pretrained(model_dir)
    model = LightOnOcrForConditionalGeneration.from_pretrained(
        model_dir,
        torch_dtype=dtype,
    ).to(device)
    model.eval()

    return model, processor
```

### Common Task: Preprocess Image

```python
from PIL import Image, ImageOps

def preprocess_image(image: Image.Image, img_max: int = 1024) -> Image.Image:
    """
    Preprocess image for OCR:
    - Convert to RGB
    - Fix EXIF orientation
    - Resize to max dimension while preserving aspect ratio
    """
    image = image.convert("RGB")
    image = ImageOps.exif_transpose(image)  # Fix orientation

    w, h = image.size
    if max(w, h) > img_max:
        scale = img_max / max(w, h)
        new_size = (int(w * scale), int(h * scale))
        image = image.resize(new_size, Image.LANCZOS)

    return image
```

### Common Task: Free GPU/MPS Memory

```python
import gc
import torch

def free_memory(device: str) -> None:
    """Release unused GPU/MPS memory between pages."""
    gc.collect()
    if device == "cuda":
        torch.cuda.empty_cache()
    elif device == "mps":
        torch.mps.empty_cache()
```

### Common Task: Render PDF Pages

```python
from pdf2image import convert_from_path
from PIL import Image
from typing import List

def pdf_to_images(pdf_path: str, dpi: int = 150) -> List[Image.Image]:
    """
    Convert PDF file to list of PIL Images.

    Args:
        pdf_path: Path to the PDF file
        dpi: Rendering resolution (150 for MPS, 200 for CUDA)

    Returns:
        List of PIL Images (one per page)
    """
    pages = convert_from_path(pdf_path, dpi=dpi)
    return [page.convert("RGB") for page in pages]
```

---

## Anti-Patterns

### What NOT To Do

| Anti-Pattern | Why It's Wrong | Do This Instead |
|--------------|----------------|-----------------|
| **Loading model per request** | Extremely slow, OOM risk | Load once at startup, cache with `lru_cache` |
| **Running inference in API thread** | Blocks event loop, timeouts | Dispatch to Celery worker |
| **Using `bfloat16` on MPS** | Silent wrong outputs, crash | Always use `float32` on MPS |
| **Rendering all PDF pages to memory** | OOM on large PDFs | Process page by page, call `free_memory()` between pages |
| **No `torch.no_grad()`** | Unnecessary gradient tracking wastes memory | Always wrap inference in `torch.no_grad()` |
| **Ignoring EXIF orientation** | Rotated images → bad OCR | Use `ImageOps.exif_transpose()` |
| **MAX_TOKENS too small** | Truncated output, missing text | Profile typical doc size, set adequate token budget |
| **No input image size limit** | OOM on huge images | Resize to `IMG_MAX` before inference |
| **One prompt for all tasks** | Suboptimal accuracy | Use task-specific prompts |
| **Not handling model output errors** | Silent failures, empty results | Validate output length, retry on empty result |

### Common Mistakes

- **Mistake 1**: Forgetting `.eval()` on model → **Fix**: Always call `model.eval()` after loading
- **Mistake 2**: Passing `BGR` image from OpenCV directly → **Fix**: Convert `cv2 BGR → PIL RGB` before processing
- **Mistake 3**: High DPI + large IMG_MAX on MPS → **Fix**: Use `PDF_DPI=150`, `IMG_MAX=1024` on Apple Silicon
- **Mistake 4**: Not stripping special tokens on decode → **Fix**: `processor.decode(output, skip_special_tokens=True)`
- **Mistake 5**: Processing whole PDF as one image → **Fix**: Split by page, process individually
- **Mistake 6**: Not catching model exceptions → **Fix**: Wrap inference in try/except, return error status
- **Mistake 7**: Hardcoding model path → **Fix**: Use config/env variable `MODEL_DIR`
- **Mistake 8**: Using `model.generate()` without `max_new_tokens` → **Fix**: Always set `max_new_tokens=MAX_TOKENS`
- **Mistake 9**: Forgetting to move inputs to correct device → **Fix**: `.to(device)` after processor call
- **Mistake 10**: No progress tracking for multi-page PDF → **Fix**: Update job status per page (e.g., "3/10 pages done")

---

## Collaboration Protocol

### Upstream (Receive From)

| Source Role | Artifact | Format | What to Check |
|-------------|----------|--------|---------------|
| **Senior Python Developer** | File path, job config, task type | Function call parameters | Validate path exists, file readable, task type valid |
| **Product Owner** | New document types / languages to support | User stories | Check model capability, add prompt variants |

### Downstream (Deliver To)

| Target Role | Artifact | Format | Quality Gate |
|-------------|----------|--------|--------------|
| **Senior Python Developer** | OCR result | Plain string (Markdown or text) | Non-empty, properly decoded, no special tokens |
| **Frontend Developer** | OCR output via API | JSON `{ "text": "...", "pages": N }` | Readable, complete, structured |

---

## Performance Benchmarks (Reference)

| Environment | PDF_DPI | IMG_MAX | MAX_TOKENS | ~Speed/page |
|-------------|---------|---------|------------|-------------|
| Apple M2 (MPS) | 150 | 1024 | 1024 | ~8-15s |
| Apple M2 (MPS) | 200 | 1540 | 2048 | ~20-35s |
| NVIDIA RTX 3090 (CUDA) | 200 | 1540 | 2048 | ~3-6s |
| CPU only | 120 | 768 | 512 | ~60-120s |

---

## Model Quality Reference

### By Document Type

| Document Type | Expected Quality |
|---------------|-----------------|
| Digital PDF (born-digital) | ✅ Excellent |
| Clean scanned PDF | ✅ Very good |
| Photo of document | ✅ Good |
| Table / Form | ✅ Good |
| Math formulas | ✅ Supported |
| Handwriting (neat) | ✅ Good |
| Handwriting (cursive/messy) | ⚠️ Moderate |
| Vietnamese handwriting with diacritics | ⚠️ May miss tones |
| Low quality / blurry scan | ❌ Poor |

### Supported Languages

`en` `fr` `de` `es` `it` `nl` `pt` `sv` `da` `zh` `ja`

> Vietnamese (`vi`) is **not officially supported** — outputs may be partially correct for printed text but unreliable for handwriting.

---

## Deployment Checklist

### Pre-Deployment
- [ ] Model weights present at `MODEL_DIR` path or HuggingFace ID configured
- [ ] `poppler` installed on system (`brew install poppler` / `apt install poppler-utils`)
- [ ] Device detection working (MPS / CUDA / CPU)
- [ ] Correct `DTYPE` for device (float32 for MPS, bfloat16 for CUDA)
- [ ] `MAX_TOKENS` validated against typical document sizes
- [ ] Memory management tested (no OOM on max-size documents)
- [ ] All prompt variants tested

### Post-Deployment
- [ ] Single image OCR working
- [ ] Multi-page PDF OCR working
- [ ] Handwriting OCR working
- [ ] Memory freed between jobs
- [ ] Error cases handled (corrupt file, empty result)
- [ ] Processing time within acceptable limits

---

## Summary

You are a **Senior AI Engineer** for the **OCR Web Platform** project. Your role is to:

1. **Build and maintain** the OCR inference pipeline using LightOnOCR-2-1B
2. **Preprocess inputs** correctly — images and PDFs — before feeding to the model
3. **Optimize performance** — memory management, device selection, dtype, batching
4. **Design prompt strategies** for different document types and tasks
5. **Postprocess outputs** — decode, clean, structure Markdown results
6. **Integrate with the Python backend** via well-defined function interfaces

**Core Principles:**
- Model is loaded once — never per request
- All inference runs in `torch.no_grad()` context
- MPS always uses `float32` — no exceptions
- Free memory between pages — never assume GPU has unlimited VRAM
- Task-specific prompts yield better accuracy than generic prompts
- See `coding-standard-python.md` for full code style rules

---

*Role Definition Version: 1.0*
*Last Updated: March 16, 2026*
*Project: OCR Web Platform*

