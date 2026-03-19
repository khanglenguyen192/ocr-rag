from pydantic import BaseModel
from datetime import datetime, timezone
from typing import TypeVar, Generic

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    success: bool = True
    message: str = "OK"
    data: T | None = None
    timestamp: datetime = None  # type: ignore[assignment]

    def model_post_init(self, __context):  # type: ignore[override]
        if self.timestamp is None:
            object.__setattr__(self, "timestamp", datetime.now(timezone.utc))


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    detail: str | None = None

