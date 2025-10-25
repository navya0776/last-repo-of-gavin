import pytest
from data.migrations import migration_001_create_base_collections as base_mig

@pytest.mark.asyncio
async def test_upgrade_idempotent(mongo_manager):
    db = mongo_manager._database
    await base_mig.upgrade(db)
    await base_mig.upgrade(db)

    cols = await db.list_collection_names()
    for name in ["All_Stores", "All_Equiments", "All_Parts"]:
        assert name in cols

    await base_mig.downgrade(db)
    cols_after = await db.list_collection_names()
    for name in ["All_Stores", "All_Equiments", "All_Parts"]:
        assert name not in cols_after
