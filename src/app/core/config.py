from pydantic_settings import BaseSettings
from functools import lru_cache
import torch


class Settings(BaseSettings):
    # App
    APP_NAME: str = "OCR Web Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database (PostgreSQL)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/pgocr"

    # Model (LightOnOCR-2-1B)
    MODEL_DIR: str = "LightOnOCR-2-1B"
    PDF_DPI: int = 150
    IMG_MAX: int = 1024
    MAX_TOKENS: int = 1024

    # File upload
    MAX_FILE_SIZE_MB: int = 50
    UPLOAD_DIR: str = "uploads"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    model_config = {"env_file": ".env", "case_sensitive": True}

    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    @property
    def device(self) -> str:
        if torch.backends.mps.is_available():
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
        return "cpu"

    @property
    def dtype(self) -> torch.dtype:
        return torch.float32 if self.device == "mps" else torch.bfloat16


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

