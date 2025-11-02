from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "postgresql+psycopg://admin:pass@localhost:5432/ims"

# Create async engine
# NOTE: Set this as the total pgadmin max_connections : (num of gunicorn workers) * (pool_size + max_overflow)
# For this cause, max_connections: (num of gunicorn workers (most prob between 2-4) * 10)
engine = create_async_engine(
    DATABASE_URL,
    pool_size=8,  # steady concurrent connections per worker
    max_overflow=2,  # temporary burst connections
    pool_pre_ping=True,  # detect broken connections
    echo=False,
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
