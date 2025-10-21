from pymongo.errors import CollectionInvalid, DuplicateKeyError

# Use this function, when a new store is being registered.


async def register_new_store(db, store_id: str, location: str, authority: str):
    try:
        await db["All_Stores"].insert_one(
            {"store_id": store_id, "location": location, "authority": authority}
        )
    except DuplicateKeyError:
        print(f"Store {store_id} already exists in All_Stores.")

    collection_name = f"store_{store_id}"
    if collection_name not in await db.list_collection_names():
        try:
            await db.create_collection(collection_name)
            await db[collection_name].create_index("equipment_code")
            await db[collection_name].creat_index("ledgers.ledger_page")
            print(f"Created collection {collection_name} with index on equipment_code.")
        except CollectionInvalid:
            print(f"Collection {collection_name} already exists.")
    else:
        print(f"Collection {collection_name} already exists.")
