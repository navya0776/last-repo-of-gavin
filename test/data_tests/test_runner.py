import pytest

@pytest.mark.asyncio
async def test_runner_applies_migrations(mongo_manager):
    from data.migrations import migration_001_create_base_collections as base_mig
    from data.migrations import migration_002_create_provisioning_collections as prov_mig

    await base_mig.upgrade(mongo_manager._database)
    await prov_mig.upgrade(mongo_manager._database)

    expected = ["All_Stores", "All_Equipments", "All_Parts", "All_Demands", "migrations"]
    cols = await mongo_manager._database.list_collection_names()
    for c in expected:
        assert c in cols
