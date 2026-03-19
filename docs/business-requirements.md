# Business Requirements — OCR Web Platform

**Version:** 1.0  
**Last Updated:** March 16, 2026  
**Status:** Active

---

## 1. Tổng quan hệ thống

OCR Web Platform là dịch vụ backend REST API cho phép convert nhiều loại nguồn dữ liệu (PDF, ảnh, video YouTube) thành văn bản định dạng Markdown để trả về cho frontend hoặc tải xuống file `.md`.

---

## 2. Nguồn dữ liệu đầu vào (Input Sources)

| Loại | Mô tả | Engine xử lý |
|------|-------|-------------|
| **PDF văn bản** | PDF dạng digital (có thể select text) | `pymupdf4llm` |
| **PDF scan** | PDF từ máy scan, không select được text | `LightOnOCR-2-1B` |
| **Ảnh** | JPEG, PNG, BMP, WebP, TIFF | `LightOnOCR-2-1B` |
| **YouTube URL** | Link video YouTube hợp lệ | `youtube_transcript_api` |

---

## 3. Luồng nghiệp vụ (Business Flows)

### 3.1 Flow A — PDF Văn bản (Digital PDF)

```
User upload PDF
    → Validate file (MIME, size ≤ 50MB, extension)
    → Lưu file tạm vào UPLOAD_DIR
    → Tạo OcrJob (status=PENDING) trong DB
    → Dispatch Celery task: run_pdf_digital(job_id, file_path)
    → Trả về job_id (HTTP 202 Accepted)

[Celery Worker]
    → pymupdf4llm.to_markdown(file_path)
    → Update OcrJob (status=DONE, result_md=...)
    → Xoá file tạm

[Client polling]
    → GET /api/v1/jobs/{job_id}
    → Khi status=DONE: nhận result_md
    → (Tuỳ chọn) GET /api/v1/jobs/{job_id}/download → tải file .md
```

### 3.2 Flow B — PDF Scan / Ảnh (OCR)

```
User upload PDF scan hoặc ảnh
    → Validate file (MIME, size ≤ 50MB)
    → Lưu file tạm
    → Tạo OcrJob (status=PENDING)
    → Dispatch Celery task: run_scanned_ocr(job_id, file_path)
    → Trả về job_id (HTTP 202)

[Celery Worker]
    → Nếu PDF: render từng trang → list PIL Image (pypdfium2, DPI=150)
    → Nếu ảnh: load PIL Image
    → Với mỗi ảnh:
        ├── preprocess: resize (IMG_MAX=1024), fix orientation
        ├── ocr_image(img) via LightOnOCR-2-1B
        └── free_memory() sau mỗi trang
    → merge_pages() → Markdown hoàn chỉnh
    → Update OcrJob (status=DONE, result_md=...)
    → Xoá file tạm

[Client polling]
    → GET /api/v1/jobs/{job_id}
```

### 3.3 Flow C — YouTube Transcript

```
User gửi YouTube URL
    → Validate URL (youtube.com/watch?v=... hoặc youtu.be/...)
    → Extract video_id
    → Tạo OcrJob (status=PENDING, source_ref=url)
    → Dispatch Celery task: run_youtube(job_id, video_id)
    → Trả về job_id (HTTP 202)

[Celery Worker]
    → YouTubeTranscriptApi().fetch(video_id, languages=['vi','en',...])
    → Format transcript → Markdown (với timestamp)
    → Update OcrJob (status=DONE, result_md=...)

[Client polling]
    → GET /api/v1/jobs/{job_id}
```

### 3.4 Flow D — Tải xuống Markdown

```
GET /api/v1/jobs/{job_id}/download
    → Kiểm tra job tồn tại và status=DONE
    → Stream result_md dưới dạng file
    → Headers:
        Content-Type: text/markdown; charset=utf-8
        Content-Disposition: attachment; filename="{job_id}.md"
```

---

## 4. API Endpoints

### Base URL: `/api/v1`

| Method | Path | Description | Request | Response |
|--------|------|-------------|---------|----------|
| `POST` | `/pdf/digital` | Upload PDF văn bản | `multipart/form-data` (file) | `OcrJobResponse` 202 |
| `POST` | `/pdf/scanned` | Upload PDF scan | `multipart/form-data` (file) | `OcrJobResponse` 202 |
| `POST` | `/ocr/image` | Upload ảnh | `multipart/form-data` (file) | `OcrJobResponse` 202 |
| `POST` | `/youtube/transcript` | YouTube URL | `{"url": "..."}` | `OcrJobResponse` 202 |
| `GET` | `/jobs/{job_id}` | Kiểm tra trạng thái job | — | `OcrJobResponse` |
| `GET` | `/jobs/{job_id}/download` | Tải file .md | — | `text/markdown` file |
| `GET` | `/jobs` | Danh sách jobs gần đây | `?page=1&size=20` | `PageResponse[OcrJobResponse]` |
| `GET` | `/health` | Health check | — | `{"status": "ok"}` |

---

## 5. Data Model — OcrJob (PostgreSQL)

> Schema source-of-truth: `src/scripts/create_tables.sql`  
> SQLAlchemy model mirrors schema: `src/app/models/ocr_job.py`

| Cột | Kiểu SQL | Mô tả |
|-----|----------|-------|
| `id` | `SERIAL PRIMARY KEY` | Auto-increment ID |
| `job_type` | `VARCHAR(20) NOT NULL` | `pdf_digital` / `pdf_scanned` / `image` / `youtube` |
| `source_ref` | `TEXT NOT NULL` | Tên file gốc hoặc YouTube URL |
| `original_filename` | `VARCHAR(500)` | Tên file người dùng upload (nullable) |
| `result_md` | `TEXT` | Kết quả Markdown (nullable) |
| `page_count` | `INTEGER DEFAULT 0` | Số trang đã xử lý |
| `created_at` | `TIMESTAMP DEFAULT NOW()` | Thời điểm tạo |

### Khởi tạo DB

```bash
psql -U postgres -d pgocr -f src/scripts/create_tables.sql
```

## 6. Cấu hình hệ thống (Configuration)

| Biến môi trường | Mặc định | Ý nghĩa |
|----------------|---------|---------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./ocr.db` | DB connection string |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis broker cho Celery |
| `MODEL_DIR` | `LightOnOCR-2-1B` | Đường dẫn hoặc HuggingFace ID của model |
| `UPLOAD_DIR` | `uploads/` | Thư mục lưu file tạm |
| `PDF_DPI` | `150` | DPI render PDF (MPS: 150, CUDA: 200) |
| `IMG_MAX` | `1024` | Cạnh dài tối đa ảnh đưa vào OCR (px) |
| `MAX_TOKENS` | `1024` | Token tối đa OCR mỗi ảnh |
| `MAX_FILE_SIZE_MB` | `50` | Giới hạn kích thước file upload |

---

## 8. Giới hạn và ràng buộc

### File upload
- Kích thước tối đa: **50 MB**
- Định dạng PDF hỗ trợ: `.pdf`
- Định dạng ảnh hỗ trợ: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`, `.tiff`
- Validate MIME type bằng magic bytes (không chỉ extension)

### YouTube
- URL hợp lệ: `youtube.com/watch?v=ID` hoặc `youtu.be/ID`
- Video phải có phụ đề (CC) — nếu không có sẽ trả về lỗi `422`
- Ngôn ngữ ưu tiên: `vi`, `en` (fallback sang ngôn ngữ khác nếu không có)

### OCR
- Ngôn ngữ model hỗ trợ: `en, fr, de, es, it, nl, pt, sv, da, zh, ja`
- Tiếng Việt in: nhận diện tốt hơn handwriting
- Chữ viết tay tiếng Việt có dấu: có thể thiếu dấu

---

## 9. Non-functional Requirements

| Yêu cầu | Mục tiêu |
|---------|---------|
| API response time | < 200ms (không tính OCR processing) |
| OCR throughput | Tuỳ device: MPS ~10s/trang, CUDA ~4s/trang, CPU ~90s/trang |
| Concurrent uploads | Hỗ trợ nhiều job song song (mỗi job 1 Celery task) |
| File cleanup | Xoá file tạm sau khi xử lý xong |
| Logging | Log mọi request + job lifecycle |
| Health check | `GET /health` trả về trong mọi trường hợp |

---

## 10. Out of Scope (MVP)

- Authentication / Authorization (JWT, OAuth) — thêm sau
- User management
- Quota / rate limiting per user
- Fine-tuning model
- Xử lý real-time streaming kết quả OCR (WebSocket/SSE) — thêm sau
- Hỗ trợ Word (.docx), Excel (.xlsx) — thêm sau

---

*Business Requirements Version: 1.0*  
*Project: OCR Web Platform*

