import pytest
import pytest_asyncio
import uuid
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

from data.migrations import migration_002_create_provisioning_collections as prov_mig

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
async def test_upgrade_and_downgrade(db):
    await prov_mig.upgrade(db)

    cols = await db.list_collection_names()
    assert "All_Demands" in cols

    indexes = await db["All_Demands"].index_information()
    assert "demand_number_1" in indexes
    assert "details.ledger_page_number_1" in indexes

    await prov_mig.downgrade(db)

    cols_after = await db.list_collection_names()
    assert "All_Demands" not in cols_after
