from typing import Optional
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

MONGO_URI = "mongodb://localhost:27017"


class MongoManager:
    def __init__(self) -> None:
        self._client: Optional[AsyncIOMotorClient] = None
        self._database: Optional[AsyncIOMotorDatabase] = None

        # Collections
        self.users: Optional[AsyncIOMotorCollection] = None

    # A function to initalize Mongo Client and database, which returns Mongo Client
    # A `get_database()` function is not needed for this as mostly collections will be called
    async def init_client(self) -> AsyncIOMotorClient:
        self._client = AsyncIOMotorClient(MONGO_URI)
        self._database = self._client.get_database("ims")

        await self._init_collections()

        return (
            self._client
        )  # Returning `client` to gracefully close the connection at shutdown

    async def _init_collections(self):
        if self._database is None:
            raise RuntimeError("Database not initalized!")

        # Initialize all collections here
        self.users = self._database.get_collection("users")
