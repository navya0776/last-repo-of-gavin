import asyncio
from hashlib import sha256
from logging import getLogger
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.authentication import ForgetPasswordRequest, LoginRequest
from backend.core.middleware import get_current_user

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
    body: ForgetPasswordRequest,
    session: AsyncSession = Depends(get_db)
):
    user = await session.scalar(
        select(User).where(User.username == body.username)
    )

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Only first-time change allowed
    if user.new_user is False:
        raise HTTPException(
            status_code=403,
            detail="Password can only be changed during first login."
        )

    # Save new password
    user.password = sha256(body.new_password.encode()).hexdigest()
    user.new_user = False

    await session.commit()
    await session.refresh(user)

    return {"message": "Password updated successfully"}
