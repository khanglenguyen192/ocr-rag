"""
FastAPI application entry point.
"""
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.routers import pdf, ocr, youtube, jobs

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    import asyncio
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    logger.info("🚀 %s v%s started | device=%s", settings.APP_NAME, settings.APP_VERSION, settings.device)

    logger.info("⏳ Loading LightOnOCR-2-1B model at startup...")
    try:
        from app.ocr_engine.model_loader import load_model
        await asyncio.to_thread(load_model)
        logger.info("✅ LightOnOCR-2-1B model ready.")
    except Exception:
        logger.exception("❌ Failed to load LightOnOCR-2-1B at startup — will load on first call.")

    yield

    logger.info("👋 %s shutting down.", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Backend API for OCR Web Platform. "
        "Converts PDF, scanned images, and YouTube videos to Markdown."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global exception handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s %s", request.method, request.url)
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error", "detail": str(exc) if settings.DEBUG else None},
    )


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"], summary="Health check")
async def health():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


# ── Routers ───────────────────────────────────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(pdf.router, prefix=API_PREFIX)
app.include_router(ocr.router, prefix=API_PREFIX)
app.include_router(youtube.router, prefix=API_PREFIX)
app.include_router(jobs.router, prefix=API_PREFIX)
