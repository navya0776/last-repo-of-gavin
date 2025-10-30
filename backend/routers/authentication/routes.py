import asyncio
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from logging import getLogger
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from schemas.authentication import LoginRequest

from backend.core.middleware import get_current_user
from backend.repositories import UserCollection
from data.database.redis import get_redis
from data.models.users import User

app = APIRouter()
audit_logger = getLogger("audit_logs")


@app.post("/login")
async def login(credentials: LoginRequest, users: UserCollection):
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
        users.find_one({"username": username}), get_redis()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found!"
        )

    user_model = User(**user)

    # Gets user password, and matches it with SHA256 hex digest representation
    stored_password = user_model.password
    if not stored_password or stored_password != sha256(password.encode()).digest():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password!"
        )

    session_id = str(uuid4())
    expiry = datetime.now(timezone.utc) + timedelta(hours=2)

    # Set session data
    session_data = {"user_id": username, "expired": expiry.isoformat()}

    await redis.hset(
        f"session:{session_id}", mapping=session_data
    )  # pyright: ignore[reportGeneralTypeIssues]

    response = JSONResponse(
        {
            "message": "Login successful",
            "is_admin": user_model.role.role_name == "admin",
        }
    )

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=2 * 60 * 60,
    )

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
