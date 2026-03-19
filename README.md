# 🔍 OCR Python — LightOnOCR-2-1B Toolkit

Bộ công cụ OCR sử dụng **[LightOnOCR-2-1B](https://huggingface.co/lightonai/LightOnOCR-2-1B)** — model OCR end-to-end 1B tham số của [LightOn](https://lighton.ai), chuyển đổi PDF, ảnh scan, ảnh chụp thành Markdown có cấu trúc.

Bên cạnh engine chính LightOnOCR, hệ thống còn hỗ trợ **EasyOCR** (nhanh nhẹ) và **PaddleOCR** (chính xác cao, hỗ trợ trích xuất cấu trúc văn bản/bảng biểu).

---

## 📋 Mục lục

- [Tính năng](#-tính-năng)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt](#-cài-đặt)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Notebooks](#-notebooks)
- [Backend API](#-backend-api-src)
- [Cấu hình](#-cấu-hình)
- [Model Variants](#-model-variants)
- [Lưu ý về hiệu năng](#-lưu-ý-về-hiệu-năng)

---

## ✨ Tính năng

- 📄 **OCR PDF** — Chuyển toàn bộ trang PDF sang Markdown (streaming response)
- 🖼️ **OCR ảnh** — Hỗ trợ JPG, PNG, BMP, WebP, TIFF
- 🤖 **Đa Engine linh hoạt**:
  - **LightOnOCR (mặc định)**: AI 1B parametres, tốt cho viết tay và layout phức tạp.
  - **PaddleOCR**: Chính xác cao với tiếng Việt, hỗ trợ nhận diện bảng biểu & bố cục (PPStructureV3).
  - **EasyOCR**: Nhanh, nhẹ, hỗ trợ nhiều ngôn ngữ.
- ✍️ **Chữ viết tay** — Nhận diện handwriting tốt (LightOnOCR).
- 🧾 **Layout Analysis** — Trích xuất cấu trúc văn bản, bảng biểu thành Markdown (PaddleOCR Structure).
- 🎥 **YouTube Transcript** — Lấy phụ đề từ video YouTube (có sẵn hoặc auto-gen).
- 💾 **Streaming** — Trả kết quả ngay lập tức qua SSE (Server-Sent Events), không cần chờ xử lý xong toàn bộ file.
- 🍎 **Hỗ trợ Apple Silicon** — Chạy tốt trên MPS (M1/M2/M3).

---

## 💻 Yêu cầu hệ thống

| | Tối thiểu | Khuyến nghị |
|---|---|---|
| **Python** | 3.10+ | 3.11+ |
| **RAM** | 8 GB | 16 GB+ |
| **GPU VRAM** | — | 4 GB+ (CUDA/MPS) |
| **Disk** | 3 GB (model) | 5 GB+ |
| **OS** | macOS / Linux / Windows | macOS (Apple Silicon) hoặc Linux (CUDA) |

> ⚠️ Trên **Apple Silicon (MPS)**: dùng `float32`, giảm `IMG_MAX=1024` và `PDF_DPI=150` để tránh OOM crash nếu dùng LightOnOCR.

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
# Cài đặt thư viện Python (bao gồm LightOnOCR, EasyOCR, PaddleOCR...)
pip install -r src/requirements.txt
```

### 4. Tải model LightOnOCR (Tuỳ chọn)

**Cách A — Dùng model local** (đã có sẵn trong thư mục `LightOnOCR-2-1B/`):
```python
MODEL_DIR = "LightOnOCR-2-1B"   # đường dẫn local config trong .env
```

**Cách B — Tải từ HuggingFace**:
```bash
pip install huggingface_hub
huggingface-cli download lightonai/LightOnOCR-2-1B --local-dir LightOnOCR-2-1B
```

---

## 📁 Cấu trúc dự án

```
ocr-python/
├── lightonocr_tool.ipynb       # 📓 Notebook demo
├── pdf-to-markdown.ipynb       # 📓 Notebook PDF digital
├── extract-youtube-cc.ipynb    # 📓 Notebook YouTube
├── src/                        # 🚀 Backend FastAPI (production)
│   ├── app/
│   │   ├── main.py             # FastAPI entry point
│   │   ├── routers/            # API endpoints (ocr, pdf, youtube)
│   │   ├── ocr_engine/         # Logic OCR (LightOn, Paddle, EasyOCR)
│   ├── requirements.txt        # Dependencies
│   ├── .env.example            # Environment config
│   ├── docker-compose.yml      # Docker stack
│   └── Dockerfile
│
├── ui/                         # 🎨 React Frontend
├── input/                      # 📥 File đầu vào demo
├── output/                     # 📤 Kết quả demo
└── LightOnOCR-2-1B/            # 🤖 Model weights
```

---

## 🚀 Backend API (src/)

FastAPI backend xử lý OCR trực tiếp không cần Database hay Redis.

### Khởi động nhanh (local)

```bash
cd src

# 1. Copy env và chỉnh sửa nếu cần
cp .env.example .env

# 2. Chạy API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend sẽ chạy tại `http://localhost:8000`.
Truy cập Swagger UI tại `http://localhost:8000/docs` để test API.

### Khởi động với Docker Compose

```bash
cd src
docker-compose up --build
```

### API Endpoints Chính

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `POST` | `/api/v1/pdf/digital` | Convert PDF văn bản (text layer) -> Markdown (nhanh) |
| `POST` | `/api/v1/pdf/scanned` | OCR PDF scan -> Markdown (Streaming SSE) |
| `POST` | `/api/v1/ocr/image` | Upload ảnh -> Markdown |
| `POST` | `/api/v1/youtube/verify` | Kiểm tra link YouTube & lấy list ngôn ngữ |
| `POST` | `/api/v1/youtube/transcript`| Lấy transcript YouTube -> Markdown |

Tham số `engine` (cho endpoint `scanned` và `image`):
- `lighton` (default)
- `easyocr`
- `paddleocr`
- `paddleocr-structure` (layout analysis + table)

---

## ⚙️ Cấu hình

Các biến môi trường trong `.env` (hoặc `app/core/config.py`):

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `MODEL_DIR` | `"LightOnOCR-2-1B"` | Đường dẫn model LightOnOCR |
| `PDF_DPI` | `150` | Độ phân giải render PDF |
| `IMG_MAX` | `1024` | Cạnh dài tối đa của ảnh |
| `MAX_TOKENS` | `1024` | Số token tối đa LightOnOCR sinh ra |
| `UPLOAD_DIR` | `"uploads"` | Nơi lưu file tạm khi upload |

---

## 🎨 Frontend (ui/)

Giao diện React + Vite để upload file và xem kết quả trực quan.

```bash
cd ui
npm install
npm run dev
```
Truy cập `http://localhost:5173`.

---

## 📄 License

Model LightOnOCR-2-1B: **Apache License 2.0**
PaddleOCR & EasyOCR: Tuân theo license của từng thư viện tương ứng.
