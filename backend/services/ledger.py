from data.database.mongo import MongoManager
from data.models.ledgers import AllStores

ledgers = MongoManager().ledger
stores = MongoManager().all_stores


async def get_all_ledgers() -> list[AllStores]:
    docs = await stores.find({}, {"_id": 0}).to_list(None)
    return [AllStores(**doc) for doc in docs]
