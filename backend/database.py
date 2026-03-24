"""
database.py — ★ DATABASE CONNECTION POINT ★

This file sets up the async SQLAlchemy engine and session factory.
All database-dependent code imports `get_db` from here.

To switch databases, change DATABASE_URL in backend/.env:
  PostgreSQL : postgresql+asyncpg://user:pass@host:5432/dbname
  SQLite     : sqlite+aiosqlite:///./pathpilot.db  (dev only)
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings

# ── Engine ────────────────────────────────────────────────────────────
_is_sqlite = settings.DATABASE_URL.startswith("sqlite")
_engine_kwargs: dict = {"echo": settings.DEBUG}
if _is_sqlite:
    # SQLite needs check_same_thread=False for async use
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    _engine_kwargs["pool_size"] = 10
    _engine_kwargs["max_overflow"] = 20
    _engine_kwargs["pool_pre_ping"] = True

engine = create_async_engine(settings.DATABASE_URL, **_engine_kwargs)

# ── Session Factory ───────────────────────────────────────────────────
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# ── Declarative Base ──────────────────────────────────────────────────
# All models must inherit from this Base
class Base(DeclarativeBase):
    pass


# ── Dependency ────────────────────────────────────────────────────────
# Inject into FastAPI route handlers as: db: AsyncSession = Depends(get_db)
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ── Table creation (use Alembic for production) ───────────────────────
async def create_tables():
    """Create all tables. In production, prefer `alembic upgrade head`."""
    # Import all models so Base.metadata is populated before create_all
    from models import user, roadmap, test, interview  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """Drop all tables. DESTRUCTIVE — only use in development/testing."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
