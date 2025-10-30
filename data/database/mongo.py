import os

from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorCollection,
                                 AsyncIOMotorDatabase)

MONGO_URI = os.getenv(
    "MONGO_URI", "mongodb://admin:admin@localhost:27017/?authSource=admin"
)


class MongoManager:
    def __init__(self) -> None:
        self._client: AsyncIOMotorClient
        self._database: AsyncIOMotorDatabase

        self.users: AsyncIOMotorCollection
        self.logs: AsyncIOMotorCollection
        self.all_parts: AsyncIOMotorCollection
        self.all_equipments: AsyncIOMotorCollection
        self.all_stores: AsyncIOMotorCollection
        self.demands: AsyncIOMotorCollection

    async def init_client(self) -> AsyncIOMotorClient:
        self._client = AsyncIOMotorClient(MONGO_URI)
        self._database = self._client.get_database("ims")

        await self._init_collections()
        return self._client

    async def _init_collections(self):
        if self._database is None:
            raise RuntimeError("Database not initialized!")

        self.users = self._database.get_collection("Users")
        self.logs = self._database.get_collection("Audit_Logs")
        self.all_parts = self._database.get_collection("All_Parts")
        self.all_equipments = self._database.get_collection("All_Equipments")
        self.all_stores = self._database.get_collection("All_Stores")
        self.demands = self._database.get_collection("Demands")

    async def close(self):
        if self._client:
            self._client.close()


_mongo_manager: MongoManager | None = None


async def get_mongo_manager() -> MongoManager:
    """
    Dependency to get the initialized MongoManager instance.

    Returns:
        MongoManager: The initialized MongoManager singleton.

    Raises:
        RuntimeError: If MongoManager hasn't been initialized yet.
    """
    global _mongo_manager
    if _mongo_manager is None:
        _mongo_manager = None
        raise RuntimeError("MongoManager not initialized. Call init_mongo() first.")
    return _mongo_manager


async def init_mongo() -> MongoManager:
    """
    Initialize the global MongoManager singleton.

    Returns:
        MongoManager: The initialized MongoManager instance.
    """
    global _mongo_manager
    if _mongo_manager is None:
        _mongo_manager = MongoManager()
        await _mongo_manager.init_client()
    return _mongo_manager


async def close_mongo():
    """Close the global MongoManager instance."""
    global _mongo_manager
    if _mongo_manager is not None:
        await _mongo_manager.close()
        _mongo_manager = None
