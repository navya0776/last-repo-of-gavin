import asyncio
from hashlib import sha256
from logging import getLogger
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.future import select

from schemas.authentication import ForgetPasswordRequest, LoginRequest
from backend.core.middleware import get_current_user
from data.models.users import User
from data.database.redis import get_redis
from data.database import DBSession

app = APIRouter()
audit_logger = getLogger("audit_logs")
logger = getLogger(__name__)


@app.post("/login")
async def login(credentials: LoginRequest, session = DBSession):
    """
    Login route:
        1. Verify username and password.
        2. Create session in Redis.
        3. Set cookie with session_id.
    """
    username = credentials.username
    password = credentials.password

    # Query the user from PostgreSQL
    result, redis = await asyncio.gather(session.execute(select(User).where(User.username == username)), get_redis())
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found!"
        )

    # Verify password
    if user.password != sha256(password.encode()).hexdigest():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password!"
        )

    # Create session in Redis
    session_id = str(uuid4())
    await redis.hset(f"session:{session_id}", mapping={"user_id": username})

    # Build response
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
    """
    Logout route:
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
    new_user: ForgetPasswordRequest, session= DBSession
):
    """
    Reset a user's password if they are marked as a new user.
    """
    result = await session.execute(select(User).where(User.username == new_user.username))
    user = result.scalars().first()

    if not user:
        logger.critical(
            "Forget password conditions matched but user does not exist in database"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error!",
        )

    # Update password and mark as not new
    user.password = sha256(new_user.new_password.encode()).hexdigest()
    user.new_user = False

    await session.commit()

    return status.HTTP_200_OK