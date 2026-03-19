from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
import urllib.parse
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def _build_engine_url_and_args(url: str) -> tuple[str, dict]:
    """
    asyncpg không hỗ trợ query param ?options=...
    Strip nó ra và chuyển search_path vào connect_args server_settings.
    """
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    connect_args: dict = {}

    options_val = params.pop("options", [None])[0]
    if options_val:
        decoded = urllib.parse.unquote_plus(options_val)
        # e.g. "-c search_path=pgdbo"
        for part in decoded.split():
            if part.startswith("-c"):
                continue
            if "search_path=" in part:
                schema = part.split("=", 1)[1]
                connect_args["server_settings"] = {"search_path": schema}

    clean_query = urlencode(params, doseq=True)
    clean_url = urlunparse(parsed._replace(query=clean_query))
    return clean_url, connect_args


_db_url, _connect_args = _build_engine_url_and_args(settings.DATABASE_URL)

engine = create_async_engine(
    _db_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args=_connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:  # type: ignore[return]
    """FastAPI dependency — yields an async DB session per request."""
    async with AsyncSessionLocal() as session:
        yield session
