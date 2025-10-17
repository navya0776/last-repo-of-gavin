import importlib.util
import os
import sys
from pymongo import MongoClient
from pymongo.errors import OperationFailure


MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")

URI = os.getenv("DATABASE_URL", "mongodb://admin:admin@localhost:27017/ims?authSource=admin")
client = MongoClient(URI)
db = client.get_default_database()
migrations_col = db.get_collection("migrations")

def applied_names():
    return {m["name"] for m in migrations_col.find({}, {"name":1})}

def load_module(path):
    spec = importlib.util.spec_from_file_location("m", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def supports_transactions():
    try:
        info = client.server_info()
        # Transactions require replica set / WiredTiger engine; check replSet config
        return client.nodes and client.primary is not None
    except Exception:
        return False

def run_migration(module_name, module_path, use_tx):
    module = load_module(module_path)
    name = os.path.basename(module_path)
    print("Applying", name)
    if use_tx:
        with client.start_session() as session:
            with session.start_transaction():
                # migration should expose upgrade(db, session) or upgrade(db)
                if hasattr(module, "upgrade"):
                    module.upgrade(db, session)
                elif hasattr(module, "async_upgrade"):
                    raise RuntimeError("async migrations not supported in runner")
                else:
                    raise RuntimeError("migration missing upgrade(db[,session])")
                migrations_col.insert_one({"name": name})
    else:
        # no transaction
        if hasattr(module, "upgrade"):
            module.upgrade(db)
        else:
            raise RuntimeError("migration missing upgrade(db)")
        migrations_col.insert_one({"name": name})

def main():
    applied = applied_names()
    files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".py"))
    use_tx = supports_transactions()
    print("Transactions supported:", use_tx)
    for f in files:
        if f in applied:
            print("Skipping", f)
            continue
        path = os.path.join(MIGRATIONS_DIR, f)
        run_migration(f, path, use_tx)
    print("All migrations applied")

if __name__ == "__main__":
    main()
