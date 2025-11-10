import asyncio
from logging import getLogger
from hashlib import sha256

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.middleware import get_admin_user
from backend.schemas.users.permissions import Permissions
from backend.schemas.users import User as UserModel

from data.database import get_db, get_redis
from data.models.users import User
# from data.models.logs import Log  # Assuming you have a Log model now
from schemas.admin import CreateUserRequest, LogFetchRequest, LogResponse

router = APIRouter(dependencies=[Depends(get_admin_user)])
# router = APIRouter()
logger = getLogger(__name__)
audit_logger = getLogger("audit_logs")


# -----------------------------------------------------------------------------
# Endpoint: Fetch Logs
# -----------------------------------------------------------------------------
# @router.post("/logs/", response_model=list[LogResponse])
# async def return_logs(
#     logs: LogFetchRequest, 
#     session = DBSession
# ):
#     """
#     Fetch logs with optional username filtering and pagination.
#     """
#     query = select(Log).order_by(Log.created_at.desc())

#     if logs.username:
#         query = query.where(Log.username == logs.username)

#     query = query.offset(logs.start).limit(logs.end - logs.start)

#     result = await session.execute(query)
#     logs_list = result.scalars().all()

#     return [LogResponse.from_orm(log) for log in logs_list]


# -----------------------------------------------------------------------------
# Endpoint: Fetch User Details
# -----------------------------------------------------------------------------
@router.get("/users", response_model=list[UserModel])
async def get_all_users(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User))
    return result.scalars().all()


@router.get("/users/{username}", response_model=UserModel)
async def get_user(username: str, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -----------------------------------------------------------------------------
# Endpoint: Create New User
# -----------------------------------------------------------------------------
@router.post("/user")
async def create_user(
    user_creation_request: CreateUserRequest, session: AsyncSession = Depends(get_db)
):
    """
    Create a new user in the PostgreSQL database.
    """
    username = user_creation_request.username
    permissions = Permissions.model_validate(
        user_creation_request.permissions, from_attributes=True
    )

    # Check if username already exists
    result = await session.execute(select(User).where(User.username == username))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists!",
        )

    try:
        new_user = User(
            username=username,
            password=sha256(user_creation_request.password.encode()).hexdigest(),
            role=user_creation_request.role,
            new_user=True,
            permissions=permissions.model_dump(),
        )

        session.add(new_user)
    except:
        await session.rollback()
        logger.error(f"Failed to create user '{username}'", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user due to server error.",
        )

    audit_logger.info(f"Admin created new user '{username}'")
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": f"User '{username}' created successfully."},
    )


# -----------------------------------------------------------------------------
# Endpoint: Delete User
# -----------------------------------------------------------------------------
@router.delete("/user/{username}")
async def delete_user(username: str, session: AsyncSession = Depends(get_db)):
    """
    Delete a user from PostgreSQL by username.
    """
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{username}' not found!",
        )

    try:
        await session.delete(user)
    except:
        await session.rollback()
        logger.error(f"Failed to delete user '{username}'", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user '{username}' due to server error.",
        )

    audit_logger.warning(f"Admin deleted user '{username}'")

    return {"message": f"User '{username}' deleted successfully."}