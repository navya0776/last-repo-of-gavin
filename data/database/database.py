from logging import getLogger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "postgresql+psycopg://admin:pass@postgres/ims"
loggers = getLogger(__name__)

# Create async engine
# NOTE: Set this as the total pgadmin
# max_connections : (num of gunicorn workers) * (pool_size + max_overflow)
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
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.aclose()


async def init_db():
    loggers.info("Starting db session")
    async with engine.connect() as conn:
        from data.models.base import Base

            await conn.run_sync(Base.metadata.create_all)


async def close_db():
    loggers.info("Ending db session")
    await engine.dispose()
