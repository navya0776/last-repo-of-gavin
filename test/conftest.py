import pytest_asyncio
import uuid
from data.database.mongo import MongoManager
from data.database.redis import init_redis, close_redis

TEST_DB_URI = "mongodb://admin:admin@localhost:27017/?authSource=admin"


@pytest_asyncio.fixture
async def mongo_manager(monkeypatch):
    """Provide a clean test database for each test."""
    test_db_name = "ims_test_" + str(uuid.uuid4())
    monkeypatch.setenv("MONGO_DB_NAME", test_db_name)
    monkeypatch.setenv("DATABASE_URL", TEST_DB_URI)

    manager = MongoManager()
    await manager.init_client()

    # Set it as the global instance for this test
    import data.database.mongo as mongo_module

    original_manager = mongo_module._mongo_manager
    mongo_module._mongo_manager = manager

    yield manager

    # Cleanup
    await manager._client.drop_database(test_db_name)
    await manager.close()

    # Restore original
    mongo_module._mongo_manager = original_manager


@pytest_asyncio.fixture
async def redis_client(monkeypatch):
    """Provide a clean Redis instance for each test."""
    redis = await init_redis()

    # Clean up any existing test data
    await redis.flushdb()

    # Patch the global redis instance in your app
    import data.database.redis as redis_module

    original_get_redis = redis_module.get_redis
    redis_module._redis = redis

    async def override_get_redis():
        return redis

    redis_module.get_redis = override_get_redis

    yield redis

    # Cleanup after test
    await redis.flushdb()
    await close_redis()

    # Restore original get_redis
    redis_module.get_redis = original_get_redis
