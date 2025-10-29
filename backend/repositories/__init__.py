from fastapi import Depends
from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorCollection
from data.database.mongo import get_mongo_manager


async def get_users_collection() -> AsyncIOMotorCollection:
    """Get the users collection with proper type hints."""
    mongo_manager = await get_mongo_manager()
    return mongo_manager.users


async def get_audit_logs_collection() -> AsyncIOMotorCollection:
    """Get the audit logs collection"""
    mongo = await get_mongo_manager()
    return mongo.logs


# Type Annotation that basically says UserCollection is of type AsyncIOMotorCollection and stores users collection
UserCollection = Annotated[AsyncIOMotorCollection, Depends(get_users_collection)]
LogsCollection = Annotated[AsyncIOMotorCollection, Depends(get_audit_logs_collection)]
