import pytest
import pytest_asyncio
import uuid
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from data.migrations import migration_001_create_base_collections as base_mig

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
async def test_upgrade_idempotent(db):
    await base_mig.upgrade(db)
    await base_mig.upgrade(db)

    cols = await db.list_collection_names()
    assert "All_Stores" in cols
    assert "All_Equiments" in cols
    assert "All_Parts" in cols

    await base_mig.downgrade(db)

    cols_after = await db.list_collection_names()
    assert "All_Stores" not in cols_after
    assert "All_Equiments" not in cols_after
    assert "All_Parts" not in cols_after
