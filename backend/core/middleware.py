from logging import getLogger
from typing import Any

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.users import User as UserModel

from data.database import get_redis, get_db
from data.models.users import User

logger = getLogger(__name__)


async def get_current_user(session_id: str = Cookie(...)) -> dict[str, str]:
    """
    Retrieve the current authenticated user from a Redis-backed session.

    Steps:
        1. Check that the session_id cookie exists; raise 401 if missing.
        2. Fetch session data from Redis using hgetall(session:<session_id>).
            The session data is expected to contain at least: -
            "user_id": str - "expires": ISO8601 datetime string

        3. If session is not found in Redis, raise 401 (session expired/not found).
        4. Return the "user_id" string from the session.

    Args:
        session_id (str, optional): The session ID from the client's cookie.

    Returns:
        dict: A dictionary containing the authenticated user's details, e.g.:
            {
                "user_id": str,
                "session_id": str
            }

    Raises:
        HTTPException: With status code 401 in case of: - Missing session cookie - Session not found in Redis - Session expired
    """

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    redis = await get_redis()

    session_info: dict[str, Any] = await redis.hgetall(
        f"session:{session_id}"
    )  # # pyright: ignore[reportGeneralTypeIssues]

    if session_info is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found or expired",
        )

    user_id = session_info.get("user_id")
    if user_id is None:
        logger.error(
            f"Invalid Session id was generated!, user_id missing! Session ID: {session_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    return {"user_id": user_id, "session_id": session_id}


async def get_admin_user(
    session: AsyncSession = Depends(get_db),
    user: dict[str, str] = Depends(get_current_user),
) -> dict[str, str | bool]:
    """
    FastAPI dependency that validates and enriches user authentication data with admin status.

    This middleware function serves as a secondary authentication layer that:
    1. Validates that the authenticated user has a valid user_id
    2. Verifies the user exists in the database
    3. Enriches the user data with admin role information

    Args:
        users: MongoDB collection containing user documents
        user: Authenticated user dict from get_current_user dependency, containing:
            - user_id: Username/user identifier
            - session_id: Current session identifier

    Returns:
        dict containing:
            - user_id (str): The user's identifier
            - session_id (str): The current session ID
            - admin (bool): True if user has admin role, False otherwise

    Raises:
        HTTPException: 401 Unauthorized if user_id is missing from session
        AssertionError: If user passed get_current_user but doesn't exist in database
            (indicates a critical data consistency issue)


    Note:
        This function depends on get_current_user which validates the session
        in Redis before this function is called. The user dict passed here
        should always have user_id and session_id from a valid session.
    """
    user_id = user.get("user_id")

    if user_id is None:
        logger.error(
            f"Invalid Session id was generated!, user_id missing! Session ID: {user.get('session_id')}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    curr_user = await session.execute(select(User).where(User.username == user_id))

    if curr_user is None:
        logger.critical(
            f"{user_id} passed `get_current_user` function but failed `get_admin_user`"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found!"
        )

    user_model = UserModel.model_validate(curr_user)

    return {
        "user_id": user_model.username,
        "session_id": user["session_id"],
        "is_admin": user_model.role == "admin",
    }
