from middleware.setup import settings
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from sqlalchemy.orm import sessionmaker

POSTGRESQL_ASYNC_DATABASE_URL = settings["db"]["uri"]
print("__postgresql_async_database_url__", POSTGRESQL_ASYNC_DATABASE_URL)
engine = AsyncEngine(create_engine(POSTGRESQL_ASYNC_DATABASE_URL, echo=True, future=True))

async def init_db():
    async with engine.begin() as connection:
        # await connection.run_sync(SQLModel.metadata.drop_all)
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session