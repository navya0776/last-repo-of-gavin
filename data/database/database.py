from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


DBSession: Annotated[AsyncSession, Depends(get_db)]
