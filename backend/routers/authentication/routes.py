import asyncio
from datetime import datetime, timedelta
from hashlib import sha256
from logging import getLogger
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.authentication import ForgetPasswordRequest, LoginRequest
from backend.core.middleware import get_current_user
from backend.schemas.users import User as UserModel

from data.database import get_redis, get_db
from data.models.users import User

app = APIRouter()
audit_logger = getLogger("audit_logs")
logger = getLogger(__name__)


@app.post("/login")
async def login(credentials: LoginRequest, session: AsyncSession = Depends(get_db)):
    """
    Login route:
        1. Verify username and password.
        2. Create session in Redis.
        3. Set cookie with session_id.
    """
    username = credentials.username
    password = credentials.password

    # Find user by username
    user, redis = await asyncio.gather(
        session.scalar(select(User).where(User.username == username)), get_redis()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found!"
        )

    # Gets user password, and matches it with SHA256 hex digest representation
    if user.password != sha256(password.encode()).hexdigest():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password!"
        )

    session_id = str(uuid4())

    # Set session data
    session_data = {"user_id": username}

    await redis.hset(f"session:{session_id}", mapping=session_data)  # pyright: ignore[reportGeneralTypeIssues]

    response = JSONResponse(
        {
            "message": "Login successful",
            "is_admin": user.role == "admin",
            "is_new_user": user.new_user,
        }
    )

    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=None)

    return response


@app.post("/logout")
async def logout(user: dict[str, str] = Depends(get_current_user)):
    """Logout route:
    1. Delete session from Redis.
    2. Remove session cookie from client.
    """
    redis = await get_redis()
    await redis.delete(f"session:{user['session_id']}")

    response = JSONResponse({"message": "Logged out successfully"})
    response.delete_cookie("session_id")

    return response


@app.post("/forget-password")
async def forget_password(
    new_user: ForgetPasswordRequest, session: AsyncSession = Depends(get_db)
):
    """
    Reset a user's password if they are marked as a new user.

    This endpoint allows a new user to set their password for the first time.
    It validates the user's existence in the database, updates their password,
    and marks the `new_user` field as `False` after a successful reset.

    Steps:
        1. Check if the username exists in the users collection.
        2. If the user is not found, log a critical error and raise HTTP 500.
        3. If found, update the password and set `new_user` to False.
        4. Return HTTP 200 OK on success.

    Args:
        new_user (ForgetPasswordRequest): Pydantic model containing the username and new password details.
        users (UserCollection): MongoDB collection handler for user records.

    Returns:
        int: HTTP 200 OK on successful password reset.

    Raises:
        HTTPException:
            - 500 if the user record does not exist.
    """
    exists = await session.scalar(
        select(User).where(User.username == new_user.username)
    )

    if exists is None:
        logger.critical(
            "New user forget password conditions matched but user does not exist in database"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error!",
        )

    exists.new_user = False
    exists.password = sha256(new_user.new_password.encode()).hexdigest()

    return status.HTTP_200_OK
