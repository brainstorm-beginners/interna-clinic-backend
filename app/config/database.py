from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config.db_config import DATABASE_URL
from app.models.models import models_metadata


engine = create_async_engine(DATABASE_URL)

models_metadata.bind = engine


async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(models_metadata.create_all)


async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
