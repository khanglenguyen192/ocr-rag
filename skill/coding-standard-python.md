# Python Coding Standard — OCR Web Platform

> Áp dụng cho toàn bộ code Python trong project.  
> Tham chiếu bởi: `senior-python-developer.md`, `senior-ai-engineer.md`

---

## 1. Python Version & Environment

```
Python: 3.11+
Package manager: pip + requirements.txt (hoặc pyproject.toml)
Virtual env: .venv (không commit vào git)
Formatter: black (line-length = 100)
Linter: ruff
Type checker: mypy (strict mode khuyến nghị)
```

---

## 2. Project Structure Convention

```
app/
├── main.py                  # FastAPI app factory
├── core/
│   ├── config.py            # Pydantic Settings
│   ├── database.py          # SQLAlchemy async engine
│   ├── security.py          # JWT, password hashing
│   └── dependencies.py      # FastAPI DI (get_db, get_current_user)
├── models/                  # SQLAlchemy ORM models (DB layer)
├── schemas/                 # Pydantic v2 schemas (API layer)
├── routers/                 # FastAPI routers
├── services/                # Business logic (no direct DB/HTTP in models)
├── tasks/                   # Celery async tasks
├── ocr_engine/              # AI inference pipeline
│   ├── model_loader.py
│   ├── preprocessor.py
│   ├── inference.py
│   ├── postprocessor.py
│   └── pipeline.py
└── utils/                   # Shared helpers
```

---

## 3. Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| **Module/file** | `snake_case` | `ocr_service.py` |
| **Class** | `PascalCase` | `OcrJobService` |
| **Function / method** | `snake_case` | `process_pdf_file()` |
| **Variable** | `snake_case` | `job_id`, `ocr_result` |
| **Constant** | `UPPER_SNAKE_CASE` | `MAX_TOKENS`, `DEFAULT_DPI` |
| **Private method** | `_snake_case` | `_validate_file()` |
| **Type alias** | `PascalCase` | `OcrTaskType = Literal["markdown", "plain_text"]` |

---

## 4. Type Hints (Mandatory)

```python
# ✅ Always annotate function signatures
def ocr_image(
    image: Image.Image,
    task: str = "markdown",
    max_tokens: int = 1024,
) -> str:
    ...

# ✅ Use | for union types (Python 3.10+)
def get_job(job_id: int | None = None) -> OcrJob | None:
    ...

# ✅ Use TypeAlias for clarity
OcrTaskType = Literal["markdown", "plain_text", "handwriting", "table"]

# ❌ Never leave functions without type hints
def process(x, y):   # BAD
    ...
```

---

## 5. Pydantic v2 Schemas

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

# ✅ Use model_config instead of class Config
class OcrJobCreate(BaseModel):
    model_config = {"str_strip_whitespace": True}

    task_type: OcrTaskType = "markdown"
    max_tokens: int = Field(default=1024, ge=128, le=4096)

# ✅ Use field_validator for custom validation
class FileUploadRequest(BaseModel):
    filename: str

    @field_validator("filename")
    @classmethod
    def validate_extension(cls, v: str) -> str:
        allowed = {".pdf", ".jpg", ".jpeg", ".png", ".webp", ".tiff"}
        ext = Path(v).suffix.lower()
        if ext not in allowed:
            raise ValueError(f"Unsupported file type: {ext}")
        return v

# ✅ Response schema always explicit
class OcrJobResponse(BaseModel):
    id: int
    status: str
    created_at: datetime
    result: str | None = None

    model_config = {"from_attributes": True}  # replaces orm_mode=True
```

---

## 6. FastAPI Routing

```python
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.core.dependencies import get_current_user, get_db

router = APIRouter(prefix="/ocr", tags=["OCR"])

# ✅ Use proper HTTP methods and status codes
@router.post("/upload", response_model=OcrJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_file_for_ocr(
    file: UploadFile = File(...),
    task_type: str = "markdown",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OcrJobResponse:
    ...

# ✅ Use HTTPException for client errors
@router.get("/jobs/{job_id}", response_model=OcrJobResponse)
async def get_ocr_job(job_id: int, db: AsyncSession = Depends(get_db)) -> OcrJobResponse:
    job = await ocr_service.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job
```

---

## 7. SQLAlchemy 2.x (Async)

```python
from sqlalchemy import String, Integer, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

# ✅ Use Mapped + mapped_column (SQLAlchemy 2.x style)
class OcrJob(Base):
    __tablename__ = "ocr_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="PENDING")
    file_path: Mapped[str] = mapped_column(String(500))
    task_type: Mapped[str] = mapped_column(String(20), default="markdown")
    result: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now())

# ✅ Async query pattern
async def get_job_by_id(db: AsyncSession, job_id: int) -> OcrJob | None:
    result = await db.execute(select(OcrJob).where(OcrJob.id == job_id))
    return result.scalar_one_or_none()
```

---

## 8. Service Layer Pattern

```python
import logging
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

class OcrService:
    """Business logic for OCR job management."""

    async def create_job(
        self,
        db: AsyncSession,
        user_id: int,
        file_path: str,
        task_type: str = "markdown",
    ) -> OcrJob:
        logger.info("Creating OCR job for user=%d, task=%s", user_id, task_type)

        job = OcrJob(
            user_id=user_id,
            file_path=file_path,
            task_type=task_type,
            status="PENDING",
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)

        # Dispatch async task
        process_ocr_task.delay(job.id, file_path, task_type)

        return job
```

---

## 9. Celery Task Pattern

```python
from celery import Task
from app.core.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def process_ocr_task(self: Task, job_id: int, file_path: str, task_type: str) -> None:
    """
    Process OCR for a given job.
    Updates job status: PENDING → PROCESSING → DONE / FAILED
    """
    # Get fresh DB session per task
    from app.core.database import SyncSessionLocal
    with SyncSessionLocal() as db:
        try:
            job = db.get(OcrJob, job_id)
            if not job:
                logger.error("Job %d not found", job_id)
                return

            job.status = "PROCESSING"
            db.commit()

            result = run_ocr_pipeline(file_path, task_type)

            job.status = "DONE"
            job.result = result
            db.commit()

        except Exception as exc:
            logger.exception("OCR task failed for job %d", job_id)
            job.status = "FAILED"
            db.commit()
            raise self.retry(exc=exc)
```

---

## 10. Error Handling

```python
# ✅ Catch specific exceptions
try:
    result = ocr_image(image, task="markdown")
except torch.cuda.OutOfMemoryError:
    logger.error("GPU OOM during OCR")
    raise HTTPException(status_code=503, detail="Insufficient GPU memory, try smaller file")
except ValueError as e:
    logger.warning("Invalid input: %s", e)
    raise HTTPException(status_code=400, detail=str(e))
except Exception:
    logger.exception("Unexpected error during OCR")
    raise HTTPException(status_code=500, detail="Internal OCR error")

# ✅ Global exception handler in main.py
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s %s", request.method, request.url)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# ❌ Never do this
try:
    ...
except:         # BAD - catches everything including SystemExit
    pass
```

---

## 11. Logging Standard

```python
import logging

# ✅ Use module-level logger
logger = logging.getLogger(__name__)

# ✅ Log levels
logger.debug("Processing page %d/%d", current, total)    # Detailed trace
logger.info("OCR job %d completed in %.2fs", job_id, elapsed)  # Normal operations
logger.warning("File size %dMB exceeds recommended limit", size_mb)  # Degraded behavior
logger.error("Failed to process job %d: %s", job_id, str(e))  # Errors
logger.exception("Unexpected error in OCR pipeline")  # With full traceback

# ✅ Never log sensitive data
logger.info("User %d uploaded file", user_id)       # ✅
logger.info("Password: %s", password)               # ❌ NEVER
```

---

## 12. Configuration Management (pydantic-settings)

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "OCR Web Platform"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"

    # Model
    MODEL_DIR: str = "LightOnOCR-2-1B"
    PDF_DPI: int = 150
    IMG_MAX: int = 1024
    MAX_TOKENS: int = 1024

    # File upload
    MAX_FILE_SIZE_MB: int = 50
    UPLOAD_DIR: str = "uploads"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = {"env_file": ".env", "case_sensitive": True}

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

---

## 13. File Upload & Validation

```python
import magic  # python-magic for MIME detection
from pathlib import Path

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/tiff",
}
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB

async def validate_upload(file: UploadFile) -> bytes:
    """Read, validate, and return file bytes."""
    content = await file.read()

    # Size check
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="File too large (max 50MB)")

    # MIME type check (magic bytes — not just extension)
    mime = magic.from_buffer(content[:2048], mime=True)
    if mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=415, detail=f"Unsupported file type: {mime}")

    return content
```

---

## 14. API Response Format

```python
from pydantic import BaseModel
from typing import TypeVar, Generic
from datetime import datetime

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "OK"
    data: T | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PageResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int

# Usage
@router.get("/jobs", response_model=ApiResponse[PageResponse[OcrJobResponse]])
async def list_jobs(...):
    ...
```

---

## 15. Testing Standard

```python
import pytest
from httpx import AsyncClient
from app.main import app

# ✅ Async test with pytest-asyncio
@pytest.mark.asyncio
async def test_upload_pdf_success(async_client: AsyncClient, auth_headers: dict):
    with open("tests/fixtures/sample.pdf", "rb") as f:
        response = await async_client.post(
            "/ocr/upload",
            files={"file": ("sample.pdf", f, "application/pdf")},
            headers=auth_headers,
        )
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "PENDING"

# ✅ Test naming: test_{unit}_{scenario}
def test_preprocess_image_resizes_large_image():
    img = Image.new("RGB", (2000, 3000))
    result = preprocess_image(img, img_max=1024)
    assert max(result.size) <= 1024

# ✅ Use fixtures for shared setup
@pytest.fixture
def sample_image() -> Image.Image:
    return Image.new("RGB", (800, 600), color="white")
```

---

## 16. Security Checklist

- [ ] All upload endpoints require authentication
- [ ] File MIME type validated with magic bytes (not just extension)
- [ ] File size limit enforced before reading content
- [ ] JWT secret stored in environment variable
- [ ] Passwords hashed with `bcrypt` (passlib)
- [ ] No sensitive data in logs (passwords, tokens, PII)
- [ ] CORS configured for frontend domain only
- [ ] Rate limiting on upload endpoints (slowapi)
- [ ] SQL injection prevented (use SQLAlchemy ORM / parameterized queries)
- [ ] Stack traces not exposed in production error responses
- [ ] Temp files cleaned up after processing

---

## 17. Git Commit Convention

```
feat:     New feature (e.g., "feat: add handwriting OCR endpoint")
fix:      Bug fix
refactor: Code refactor without behavior change
perf:     Performance improvement
test:     Adding or fixing tests
docs:     Documentation only
chore:    Build, CI, dependency updates
```

---

*Coding Standard Version: 1.0*
*Last Updated: March 16, 2026*
*Project: OCR Web Platform*

