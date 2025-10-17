import asyncio
import importlib.util
import os

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")

URI = os.getenv(
    "DATABASE_URL", "mongodb://admin:admin@localhost:27017/ims?authSource=admin"
)
client = AsyncIOMotorClient(URI)
db = client.get_default_database()
migrations_col = db.get_collection("migrations")


async def applied_names():
    cursor = migrations_col.find({}, {"name": 1})
    return {doc["name"] async for doc in cursor}


def load_module(path):
    spec = importlib.util.spec_from_file_location("m", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


async def supports_transactions():
    try:
        info = await client.admin.command("hello")
        return info.get("setName") is not None
    except Exception:
        return False


async def run_migration(module_name, module_path, use_tx):
    module = load_module(module_path)
    name = os.path.basename(module_path)
    print("Applying", name)

    if not hasattr(module, "upgrade"):
        raise RuntimeError(f"Migration {name} missing async upgrade(db[, session])")

    if use_tx:
        async with await client.start_session() as session:
            async with session.start_transaction():
                await module.upgrade(db, session)
                await migrations_col.insert_one({"name": name}, session=session)
    else:
        await module.upgrade(db)
        await migrations_col.insert_one({"name": name})


async def main():
    applied = await applied_names()
    files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".py"))
    use_tx = await supports_transactions()
    print("Transactions supported:", use_tx)

    for f in files:
        if f in applied:
            print("Skipping", f)
            continue
        path = os.path.join(MIGRATIONS_DIR, f)
        await run_migration(f, path, use_tx)

    print("All migrations applied.")


if __name__ == "__main__":
    asyncio.run(main())
