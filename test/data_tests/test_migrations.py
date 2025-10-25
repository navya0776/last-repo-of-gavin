import pytest
from data.migrations import migration_002_create_provisioning_collections as prov_mig

@pytest.mark.asyncio
async def test_upgrade_and_downgrade(mongo_manager):
    db = mongo_manager._database
    await prov_mig.upgrade(db)

    cols = await db.list_collection_names()
    assert "All_Demands" in cols

    indexes = await db["All_Demands"].index_information()
    assert "demand_number_1" in indexes
    assert "details.ledger_page_number_1" in indexes

    await prov_mig.downgrade(db)
    cols_after = await db.list_collection_names()
    assert "All_Demands" not in cols_after
