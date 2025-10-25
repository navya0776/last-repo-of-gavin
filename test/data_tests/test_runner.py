import pytest

@pytest.mark.asyncio
async def test_runner_applies_migrations(monkeypatch, mongo_manager):
    monkeypatch.setenv("DATABASE_URL", "mongodb://admin:admin@localhost:27017/?authSource=admin")
    monkeypatch.setenv("MONGO_DB_NAME", mongo_manager._database.name)

    from data.run_migrations import main as run_main

    await run_main()

    expected = ["All_Stores", "All_Equipments", "All_Parts", "All_Demands", "migrations"]
    cols = await mongo_manager._database.list_collection_names()
    for c in expected:
        assert c in cols
