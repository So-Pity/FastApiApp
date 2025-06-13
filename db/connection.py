from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from settings import settings


url=f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_URL}"

async_engine = create_async_engine(
    url=url,
    pool_size=settings.DB_POOL_SIZE,
    echo_pool=settings.DB_ECHO_POOL
)

async_session_maker = async_sessionmaker(
  bind=async_engine,
  class_=AsyncSession,
  expire_on_commit=False
)