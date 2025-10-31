import pytest
import uuid
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException


from backend.core.middleware import get_current_user


@pytest.mark.asyncio
class TestGetCurrentUser:
    """Test suite for get_current_user dependency function."""

    async def test_missing_session_id_raises_401(self):
        """Test that missing session_id cookie raises 401 Unauthorized."""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(session_id=None)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Not authenticated"

    async def test_empty_session_id_raises_401(self):
        """Test that empty session_id cookie raises 401 Unauthorized."""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(session_id="")

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Not authenticated"

    async def test_session_not_found_in_redis_raises_401(self, redis_client):
        """Test that non-existent session in Redis raises 401."""
        session_id = str(uuid.uuid4())

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(session_id=session_id)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Not authenticated"

    async def test_valid_session_returns_user_info(self, redis_client):
        """Test that valid session returns user_id and session_id."""
        session_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())

        # Create a valid session
        session_data = {"user_id": user_id}

        await redis_client.hset(f"session:{session_id}", mapping=session_data)

        result = await get_current_user(session_id=session_id)

        assert result == {"user_id": user_id, "session_id": session_id}

        # Verify session still exists in Redis
        session_exists = await redis_client.exists(f"session:{session_id}")
        assert session_exists == 1

    async def test_session_with_additional_fields_returns_correctly(self, redis_client):
        """Test that session with additional fields returns only user_id and session_id."""
        session_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())

        session_data = {"user_id": user_id}

        await redis_client.hset(f"session:{session_id}", mapping=session_data)

        result = await get_current_user(session_id=session_id)

        # Should only return user_id and session_id
        assert result == {"user_id": user_id, "session_id": session_id}

    async def test_concurrent_session_requests(self, redis_client):
        """Test multiple concurrent requests with the same valid session."""
        session_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())

        # Create a valid session
        session_data = {"user_id": user_id}

        await redis_client.hset(f"session:{session_id}", mapping=session_data)

        # Simulate concurrent requests
        import asyncio

        results = await asyncio.gather(
            get_current_user(session_id=session_id),
            get_current_user(session_id=session_id),
            get_current_user(session_id=session_id),
        )

        # All requests should succeed
        for result in results:
            assert result == {"user_id": user_id, "session_id": session_id}
