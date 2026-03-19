# 🔍 OCR Python — LightOnOCR-2-1B Toolkit

Bộ công cụ OCR sử dụng **[LightOnOCR-2-1B](https://huggingface.co/lightonai/LightOnOCR-2-1B)** — model OCR end-to-end 1B tham số của [LightOn](https://lighton.ai), chuyển đổi PDF, ảnh scan, ảnh chụp thành Markdown có cấu trúc.

---

## 📋 Mục lục

- [Tính năng](#-tính-năng)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt](#-cài-đặt)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Notebooks](#-notebooks)
- [Cách sử dụng](#-cách-sử-dụng)
- [Cấu hình](#-cấu-hình)
- [Model Variants](#-model-variants)
- [Lưu ý về hiệu năng](#-lưu-ý-về-hiệu-năng)

---

## ✨ Tính năng

- 📄 **OCR PDF** — Chuyển toàn bộ trang PDF sang Markdown (streaming, không mất dữ liệu nếu crash)
- 🖼️ **OCR ảnh** — Hỗ trợ JPG, PNG, BMP, WebP, TIFF
- ✍️ **Chữ viết tay** — Nhận diện handwriting với prompt tối ưu
- 🧾 **Đa dạng layout** — Bảng biểu, form, hoá đơn, nhiều cột, ký hiệu toán học
- 🌍 **Đa ngôn ngữ** — en, fr, de, es, it, nl, pt, sv, da, zh, ja
- 💾 **Lưu kết quả** — Tự động ghi ra file `.md` theo từng trang
- 🍎 **Hỗ trợ Apple Silicon** — Chạy trên MPS (M1/M2/M3) với float32

---

## 💻 Yêu cầu hệ thống

| | Tối thiểu | Khuyến nghị |
|---|---|---|
| **Python** | 3.10+ | 3.11+ |
| **RAM** | 8 GB | 16 GB+ |
| **GPU VRAM** | — | 4 GB+ (CUDA/MPS) |
| **Disk** | 3 GB (model) | 5 GB+ |
| **OS** | macOS / Linux / Windows | macOS (Apple Silicon) hoặc Linux (CUDA) |

> ⚠️ Trên **Apple Silicon (MPS)**: dùng `float32`, giảm `IMG_MAX=1024` và `PDF_DPI=150` để tránh OOM crash.

---

## 🚀 Cài đặt

### 1. Clone hoặc tải project

```bash
git clone <repo-url>
cd ocr-python
```

### 2. Tạo môi trường ảo

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# hoặc: .venv\Scripts\activate  # Windows
```

### 3. Cài đặt dependencies

```bash
pip install -r requirement.txt
```

> **Lưu ý:** `transformers>=5.0.0` là bắt buộc để hỗ trợ `LightOnOcrForConditionalGeneration`.

### 4. Tải model

**Cách A — Dùng model local** (đã có sẵn trong thư mục `LightOnOCR-2-1B/`):
```python
MODEL_DIR = "LightOnOCR-2-1B"   # đường dẫn local
```

**Cách B — Tải từ HuggingFace**:
```bash
pip install huggingface_hub
huggingface-cli download lightonai/LightOnOCR-2-1B --local-dir LightOnOCR-2-1B
```
```python
MODEL_DIR = "lightonai/LightOnOCR-2-1B"   # tải online
```

---

## 📁 Cấu trúc dự án

```
ocr-python/
├── lightonocr_tool.ipynb       # 📓 Notebook — OCR với LightOnOCR-2-1B
├── pdf-to-markdown.ipynb       # 📓 Notebook — PDF → Markdown
├── extract-youtube-cc.ipynb    # 📓 Notebook — Trích xuất phụ đề YouTube
├── requirement.txt             # 📦 Dependencies (notebooks)
├── README.md                   # 📖 Tài liệu này
│
├── docs/                       # 📋 Tài liệu nghiệp vụ
│   └── business-requirements.md
│
├── skill/                      # 🧠 AI role definitions
│   ├── senior-python-developer.md
│   ├── senior-ai-engineer.md
│   └── coding-standard-python.md
│
├── LightOnOCR-2-1B/            # 🤖 Model local (từ HuggingFace)
│   ├── model.safetensors
│   ├── config.json
│   └── ...
│
├── src/                        # 🚀 Backend FastAPI (production)
│   ├── app/
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── core/               # Config, DB, dependencies
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic v2 schemas
│   │   ├── routers/            # API route handlers
│   │   ├── services/           # Business logic
│   │   ├── tasks/              # Celery async tasks
│   │   ├── ocr_engine/         # AI inference pipeline
│   │   └── utils/              # File helpers, YouTube utils
│   ├── alembic/                # Database migrations
│   ├── tests/                  # Pytest test suite
│   ├── requirements.txt        # Backend dependencies
│   ├── .env.example            # Environment variable template
│   ├── docker-compose.yml      # Docker stack (API + Worker + Redis)
│   └── Dockerfile
│
├── input/                      # 📥 File đầu vào (notebooks)
└── output/                     # 📤 Kết quả Markdown (notebooks)
```

---

## 🚀 Backend API (src/)

FastAPI backend với Celery job queue — dùng cho production.

### Khởi động nhanh (local)

```bash
cd src

# 1. Copy env
cp .env.example .env
# Chỉnh MODEL_DIR nếu cần

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Chạy Redis (cần Docker)
docker run -d -p 6379:6379 redis:7-alpine

# 4. Chạy API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Chạy Celery worker (terminal khác)
celery -A app.tasks.celery_app.celery_app worker --loglevel=info --concurrency=1
```

### Khởi động với Docker Compose

```bash
cd src
docker-compose up --build
```

| Service | URL |
|---------|-----|
| **API + Swagger** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **Celery Flower** | http://localhost:5555 |

### API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/pdf/digital` | Upload PDF văn bản → Markdown |
| `POST` | `/api/v1/pdf/scanned` | Upload PDF scan → Markdown (OCR) |
| `POST` | `/api/v1/ocr/image` | Upload ảnh → Markdown (OCR) |
| `POST` | `/api/v1/youtube/transcript` | YouTube URL → Markdown transcript |
| `GET` | `/api/v1/jobs/{id}` | Poll trạng thái job |
| `GET` | `/api/v1/jobs/{id}/download` | Tải file `.md` |
| `GET` | `/api/v1/jobs` | Danh sách jobs |

### Chạy tests

```bash
cd src
pytest tests/ -v
```

---

## 📓 Notebooks

### `lightonocr_tool.ipynb` — Notebook chính

| Cell | Chức năng |
|---|---|
| **Import & Config** | Nạp thư viện, thiết lập device (MPS/CUDA/CPU), cấu hình `PDF_DPI`, `IMG_MAX`, `MAX_TOKENS` |
| **Load Model** | Nạp LightOnOCR-2-1B vào bộ nhớ (chạy 1 lần) |
| **Helper Functions** | `free_memory()`, `resize_if_needed()`, `ocr_image()`, `pdf_to_images()`, `process_file()` |
| **Chạy OCR** | OCR file PDF hoặc ảnh, ghi kết quả ra `.md` |
| **Test OCR ảnh** | Test nhanh với một ảnh cụ thể |
| **Test chữ viết tay** | OCR với prompt tối ưu cho handwriting |

### `pdf-to-markdown.ipynb`

Chuyển PDF sang Markdown sử dụng `pymupdf4llm` — nhanh hơn, không cần GPU, nhưng không OCR được ảnh scan.

### `extract-youtube-cc.ipynb`

Trích xuất phụ đề (closed captions) từ video YouTube.

---

## 🎯 Cách sử dụng

### OCR một file PDF

```python
# Trong lightonocr_tool.ipynb
input_path = "input/your-document.pdf"
output_path = "output/your-document.md"

result = process_file(input_path, output_path=output_path)
print(f"✅ Xong! → {output_path}")
```

### OCR một ảnh

```python
TEST_IMAGE = "input/your-image.png"
out_txt    = "output/your-image.md"

img = Image.open(TEST_IMAGE).convert("RGB")
result = ocr_image(img)

with open(out_txt, "w", encoding="utf-8") as f:
    f.write(result)
```

### OCR chữ viết tay

```python
HANDWRITING_IMAGE = "input/handwritten_note.jpg"
result = ocr_handwriting(HANDWRITING_IMAGE)
print(result)
```

---

## ⚙️ Cấu hình

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `MODEL_DIR` | `"LightOnOCR-2-1B"` | Đường dẫn model (local hoặc HuggingFace ID) |
| `PDF_DPI` | `150` | Độ phân giải render PDF (150→nhẹ hơn, 200→tốt hơn) |
| `IMG_MAX` | `1024` | Cạnh dài tối đa của ảnh trước khi đưa vào model (px) |
| `MAX_TOKENS` | `1024` | Số token tối đa model được sinh ra mỗi ảnh |
| `DEVICE` | tự động | `mps` / `cuda` / `cpu` |
| `DTYPE` | tự động | `float32` (MPS) / `bfloat16` (CUDA) |

> 💡 **Tối ưu chất lượng** (GPU mạnh): `PDF_DPI=200`, `IMG_MAX=1540`, `MAX_TOKENS=2048`  
> 💡 **Tránh crash MPS**: `PDF_DPI=150`, `IMG_MAX=1024`, `MAX_TOKENS=1024`

---

## 🤖 Model Variants

| Variant | Mô tả | Link |
|---|---|---|
| **LightOnOCR-2-1B** ✅ | Model tốt nhất (đang dùng) | [HuggingFace](https://huggingface.co/lightonai/LightOnOCR-2-1B) |
| LightOnOCR-2-1B-base | Base model, lý tưởng để fine-tune | [HuggingFace](https://huggingface.co/lightonai/LightOnOCR-2-1B-base) |
| LightOnOCR-2-1B-bbox | Kèm bounding box cho ảnh nhúng | [HuggingFace](https://huggingface.co/lightonai/LightOnOCR-2-1B-bbox) |
| LightOnOCR-2-1B-bbox-base | Base bbox, để fine-tune | [HuggingFace](https://huggingface.co/lightonai/LightOnOCR-2-1B-bbox-base) |
| LightOnOCR-2-1B-ocr-soup | Merged variant, robust hơn | [HuggingFace](https://huggingface.co/lightonai/LightOnOCR-2-1B-ocr-soup) |
| LightOnOCR-2-1B-bbox-soup | OCR + bbox kết hợp | [HuggingFace](https://huggingface.co/lightonai/LightOnOCR-2-1B-bbox-soup) |

---

## 📊 Lưu ý về hiệu năng

### Chữ viết tay (Handwriting)

| Trường hợp | Kết quả |
|---|---|
| Chữ in hoa rõ ràng | ✅ Tốt |
| Chữ viết tay ngay ngắn | ✅ Khá tốt |
| Chữ viết tay ngoáy/xấu | ⚠️ Có thể sai |
| Tiếng Việt có dấu viết tay | ⚠️ Có thể thiếu dấu |
| Ảnh mờ, độ phân giải thấp | ❌ Kém |

### Loại tài liệu

| Loại | Kết quả |
|---|---|
| PDF văn bản gốc (digital) | ✅ Rất tốt |
| PDF scan rõ nét | ✅ Tốt |
| Ảnh chụp tài liệu | ✅ Tốt |
| Bảng biểu, form | ✅ Tốt |
| Công thức toán học | ✅ Có hỗ trợ |
| PDF scan mờ/nghiêng | ⚠️ Trung bình |

---

## 📄 License

Model LightOnOCR-2-1B: **Apache License 2.0**

---

## 📚 Tài liệu tham khảo

- 📄 [Paper — LightOnOCR](https://arxiv.org/pdf/2601.14251)
- 📝 [Blog Post](https://huggingface.co/blog/lightonai/lightonocr-2)
- 🚀 [Demo Online](https://huggingface.co/spaces/lightonai/LightOnOCR-2-1B-Demo)
- 🤗 [HuggingFace Model](https://huggingface.co/lightonai/LightOnOCR-2-1B)
- 📊 [Dataset](https://huggingface.co/datasets/lightonai/LightOnOCR-mix-0126)

