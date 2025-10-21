import pytest
import pytest_asyncio
import os
import uuid
import sys
from motor.motor_asyncio import AsyncIOMotorClient

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

TEST_DB_URI = "mongodb://admin:admin@localhost:27017/?authSource=admin"

@pytest_asyncio.fixture
async def db():
    client = AsyncIOMotorClient(TEST_DB_URI)
    test_db_name = "ims_test_" + str(uuid.uuid4())
    db = client[test_db_name]
    yield db
    await client.drop_database(test_db_name)
    client.close()

@pytest.mark.asyncio
async def test_runner_applies_migrations(db, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", TEST_DB_URI)
    monkeypatch.setenv("MONGO_DB_NAME", db.name)

    from data.run_migrations import main as run_main

    await run_main()

    expected = ["All_Stores", "All_Equiments", "All_Parts", "All_Demands", "migrations"]
    cols = await db.list_collection_names()
    for c in expected:
        assert c in cols
