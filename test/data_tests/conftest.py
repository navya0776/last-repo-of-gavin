import pytest
import pytest_asyncio
import uuid
import os
from data.database.mongo import MongoManager
from data.database.redis import init_redis, close_redis

TEST_DB_URI = "mongodb://admin:admin@localhost:27017/?authSource=admin"

@pytest_asyncio.fixture
async def mongo_manager(monkeypatch):
    test_db_name = "ims_test_" + str(uuid.uuid4())
    monkeypatch.setenv("MONGO_DB_NAME", test_db_name)
    monkeypatch.setenv("DATABASE_URL", TEST_DB_URI)

    manager = MongoManager()
    await manager.init_client()

    yield manager

    await manager._client.drop_database(test_db_name)
    await manager.close()

@pytest_asyncio.fixture
async def redis_client():
    redis = await init_redis("redis://localhost:6379/0")
    yield redis
    await close_redis()
