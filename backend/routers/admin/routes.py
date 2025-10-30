from typing import Any

from core.middleware import get_admin_user
from fastapi import APIRouter, Depends, HTTPException
from repositories import LogsCollection, UserCollection
from schemas.admin import LogFetchRequest, LogResponse

from data.models.users import User

# Setup a router that only the admin can access
router = APIRouter(dependencies=[Depends(get_admin_user)])


@router.post("/logs/", response_model=list[LogResponse])
async def return_logs(logs: LogFetchRequest, logs_collection: LogsCollection):
    query = {"username": logs.username} if logs.username else {}

    # Calculate skip and limit
    skip = logs.start
    limit = logs.end - logs.start

    # Fetch in descending order (latest first)
    cursor = logs_collection.find(query).sort("_id", -1).skip(skip).limit(limit)

    audit_logs = await cursor.to_list(length=limit)
    return [LogResponse(**audits) for audits in audit_logs]


@router.post("/users/{username}")
async def return_user_detail(username: str | None, user_collection: UserCollection):
    query = {"username": username} if username else {}

    user_doc: list[dict[str, Any]] | None = await user_collection.find_one(query)

    if user_doc is None:
        raise HTTPException(status_code=401, detail="User not found!")

    user_models = [User(**user) async for user in user_doc]
