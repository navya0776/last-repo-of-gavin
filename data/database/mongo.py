from typing import Optional
import os
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
MONGO_URI = os.getenv(
    "MONGO_URI",
 "mongodb://admin:admin@localhost:27017/?authSource=admin"
)


class MongoManager:
    def __init__(self) -> None:
        self._client: Optional[AsyncIOMotorClient] = None
        self._database: Optional[AsyncIOMotorDatabase] = None

        self.users: Optional[AsyncIOMotorCollection] = None
        self.all_parts: Optional[AsyncIOMotorCollection] = None
        self.all_equipments: Optional[AsyncIOMotorCollection] = None
        self.all_stores: Optional[AsyncIOMotorCollection] = None
        self.demands: Optional[AsyncIOMotorCollection] = None

    async def init_client(self) -> AsyncIOMotorClient:
        self._client = AsyncIOMotorClient(MONGO_URI)
        self._database = self._client.get_database("ims")

        await self._init_collections()
        return self._client 

    async def _init_collections(self):
        if self._database is None:
            raise RuntimeError("Database not initialized!")

        self.users = self._database.get_collection("Users")
        self.all_parts = self._database.get_collection("All_Parts")
        self.all_equipments = self._database.get_collection("All_Equipments")
        self.all_stores = self._database.get_collection("All_Stores")
        self.demands = self._database.get_collection("Demands")

    async def close(self):
        if self._client:
            self._client.close()
