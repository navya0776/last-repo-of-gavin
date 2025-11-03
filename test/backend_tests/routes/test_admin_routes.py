import pytest
import pytest_asyncio
from hashlib import sha256
from uuid import uuid4
from httpx import ASGITransport, AsyncClient
from fastapi import FastAPI

from backend.routers.authentication.routes import app as auth_router
from backend.repositories import get_users_collection

from data.models.users import Permissions, User
from schemas.authentication.permissions import (
    LocalPurchaseQuotation,
    Ledger,
    LocalPurchaseOrdinance,
    LocalPurchasePay,
    LocalPurchaseQuery,
    LocalPurchaseRecieved,
    LocalPurhcaseIndent,
    LocalPurchaseAmmend,
    AdvanceProvisionDemand,
    RecieveVoucher,
    OverhaulScale,
    IssueVoucher,
)


def extract_session_id(response) -> str:
    """Extract session_id from Set-Cookie headers."""
    import re

    cookies = (
        response.headers.get_list("set-cookie")
        if hasattr(response.headers, "get_list")
        else [response.headers.get("set-cookie", "")]
    )
    for cookie in cookies:
        match = re.search(r"session_id=([^;]+)", cookie.strip())
        if match:
            return match.group(1)
    raise ValueError("No session_id found in cookies")


@pytest.fixture
def app(mongo_manager):
    """Create a FastAPI test app with auth router and dependency overrides."""

    test_app = FastAPI()

    # Override the users collection dependency
    async def override_get_users_collection():
        return mongo_manager.users

    test_app.dependency_overrides[get_users_collection] = override_get_users_collection
    test_app.include_router(auth_router)

    return test_app


@pytest.fixture
def valid_credentials():
    """Valid login credentials."""
    return User(
        username="testuser",
        password="test_password_123",
        new_user=False,
        role="admin",
        permissions=Permissions(
            ledger=Ledger(read=True, write=True),
            apd=AdvanceProvisionDemand(read=True, write=True),
            overhaul_scale=OverhaulScale(read=True, write=True),
            recieve_voucher=RecieveVoucher(read=True, write=True),
            issue_voucher=IssueVoucher(read=True, write=True),
            local_purchase_indent=LocalPurhcaseIndent(read=True, write=True),
            local_purchase_quotation=LocalPurchaseQuotation(read=True, write=True),
            local_purchase_ordinance=LocalPurchaseOrdinance(read=True, write=True),
            local_purchase_pay=LocalPurchasePay(read=True, write=True),
            local_purchase_query=LocalPurchaseQuery(read=True, write=True),
            local_purchase_recieved=LocalPurchaseRecieved(read=True, write=True),
            local_purchase_ammend=LocalPurchaseAmmend(read=True, write=True),
        ),
    ).model_dump()


@pytest_asyncio.fixture
async def mock_user(mongo_manager, valid_credentials):
    """Create and insert a mock user into the test database."""
    password: str = valid_credentials["password"]
    user_doc = User(
        username=valid_credentials["username"],
        password=sha256(password.encode()).hexdigest(),
        role="admin",
        new_user=False,
        permissions=Permissions(
            ledger=Ledger(read=True, write=True),
            apd=AdvanceProvisionDemand(read=True, write=True),
            overhaul_scale=OverhaulScale(read=True, write=True),
            recieve_voucher=RecieveVoucher(read=True, write=True),
            issue_voucher=IssueVoucher(read=True, write=True),
            local_purchase_indent=LocalPurhcaseIndent(read=True, write=True),
            local_purchase_quotation=LocalPurchaseQuotation(read=True, write=True),
            local_purchase_ordinance=LocalPurchaseOrdinance(read=True, write=True),
            local_purchase_pay=LocalPurchasePay(read=True, write=True),
            local_purchase_query=LocalPurchaseQuery(read=True, write=True),
            local_purchase_recieved=LocalPurchaseRecieved(read=True, write=True),
            local_purchase_ammend=LocalPurchaseAmmend(read=True, write=True),
        ),
    ).model_dump()
    await mongo_manager.users.insert_one(user_doc)
    return user_doc


@pytest.mark.asyncio
class TestLoginRoute:
    """Test suite for /login endpoint."""

    async def test_successful_login(
        self, app, mock_user, redis_client, valid_credentials
    ):
        """Test successful login flow."""
        # Make login request
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
            follow_redirects=True,
        ) as client:
            response = await client.post("/login", json=valid_credentials)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Login successful"
        assert "is_admin" in response_data

        # Verify session cookie is set - check Set-Cookie header
        set_cookie_header = response.headers.get("set-cookie", "")
        assert "session_id=" in set_cookie_header

        # Extract session_id from Set-Cookie header
        session_id = extract_session_id(response)

        # Verify session exists in Redis
        session_key = f"session:{session_id}"
        session_exists = await redis_client.exists(session_key)
        assert session_exists == 1

        # Verify session data
        session_data = await redis_client.hgetall(session_key)
        assert session_data["user_id"] == valid_credentials["username"]

        # Cleanup
        await redis_client.delete(session_key)

    async def test_login_user_not_found(self, app, mongo_manager, redis_client):
        """Test login with non-existent username."""
        credentials = {"username": "nonexistent_user", "password": "any_password"}

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/login", json=credentials)

        assert response.status_code == 401
        assert response.json()["detail"] == "User not found!"

        # Verify no session was created
        sessions = await redis_client.keys("session:*")
        assert len(sessions) == 0

    async def test_login_incorrect_password(
        self, app, mock_user, redis_client, valid_credentials
    ):
        """Test login with incorrect password."""
        credentials = {
            "username": valid_credentials["username"],
            "password": "wrong_password",
        }

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/login", json=credentials)

        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect password!"

        # Verify no session was created
        sessions = await redis_client.keys("session:*")
        assert len(sessions) == 0

    async def test_login_missing_username(self, app):
        """Test login with missing username."""
        credentials = {"password": "test_password"}

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/login", json=credentials)

        assert response.status_code == 422  # Validation error

    async def test_login_missing_password(self, app):
        """Test login with missing password."""
        credentials = {"username": "testuser"}

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/login", json=credentials)

        assert response.status_code == 422  # Validation error

    async def test_login_empty_credentials(self, app):
        """Test login with empty credentials."""
        credentials = {"username": "", "password": ""}

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/login", json=credentials)

        # Should either fail validation or fail to find user
        assert response.status_code in [401, 422]

    async def test_login_creates_unique_sessions(
        self, app, mock_user, redis_client, valid_credentials
    ):
        """Test that multiple logins create unique session IDs."""
        # Login twice
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response1 = await client.post("/login", json=valid_credentials)
            response2 = await client.post("/login", json=valid_credentials)

        assert response1.status_code == 200
        assert response2.status_code == 200

        session_id1 = extract_session_id(response1)
        session_id2 = extract_session_id(response2)

        # Session IDs should be different
        assert session_id1 != session_id2

        # Both sessions should exist in Redis
        assert await redis_client.exists(f"session:{session_id1}") == 1
        assert await redis_client.exists(f"session:{session_id2}") == 1

        # Cleanup
        await redis_client.delete(f"session:{session_id1}")
        await redis_client.delete(f"session:{session_id2}")

    async def test_login_case_sensitive_username(
        self, app, mock_user, redis_client, valid_credentials
    ):
        """Test that username is case-sensitive."""
        credentials = {
            "username": "TESTUSER",  # Different case
            "password": valid_credentials["password"],
        }

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/login", json=credentials)

        assert response.status_code == 401
        assert response.json()["detail"] == "User not found!"


@pytest.mark.asyncio
class TestLogoutRoute:
    """Test suite for /logout endpoint."""

    async def test_successful_logout(
        self, app, mock_user, redis_client, valid_credentials
    ):
        """Test successful logout flow."""
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            login_response = await client.post("/login", json=valid_credentials)
            session_id = extract_session_id(login_response)

            # Verify session exists
            assert await redis_client.exists(f"session:{session_id}") == 1

            # Set cookies on client
            client.cookies.set("session_id", session_id)

            # Logout
            logout_response = await client.post("/logout")

        assert logout_response.status_code == 200
        assert logout_response.json() == {"message": "Logged out successfully"}

        # Verify session was deleted from Redis
        assert await redis_client.exists(f"session:{session_id}") == 0

    async def test_logout_without_session(self, app):
        """Test logout without a session cookie."""
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/logout")

        # FastAPI returns 422 when required Cookie parameter is missing
        assert response.status_code == 422

    async def test_logout_with_invalid_session(self, app, redis_client):
        """Test logout with invalid/non-existent session ID."""
        fake_session_id = str(uuid4())

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            client.cookies.set("session_id", fake_session_id)
            response = await client.post("/logout")

        assert response.status_code == 401  # Should fail authentication

    async def test_multiple_logouts_same_session(
        self, app, mock_user, redis_client, valid_credentials
    ):
        """Test that logging out twice with same session fails on second attempt."""
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            login_response = await client.post("/login", json=valid_credentials)
            session_id = extract_session_id(login_response)

            # Set cookies
            client.cookies.set("session_id", session_id)

            # First logout
            first_logout = await client.post("/logout")
            assert first_logout.status_code == 200

            # Second logout with same session
            second_logout = await client.post("/logout")
            assert second_logout.status_code == 401  # Session no longer exists


@pytest.mark.asyncio
class TestLoginLogoutIntegration:
    """Integration tests for login/logout flow."""

    async def test_full_login_logout_cycle(
        self, app, mock_user, redis_client, valid_credentials
    ):
        """Test complete login and logout cycle."""
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Login
            login_response = await client.post("/login", json=valid_credentials)
            assert login_response.status_code == 200
            session_id = extract_session_id(login_response)

            # Verify session exists
            assert await redis_client.exists(f"session:{session_id}") == 1

            # Set cookies
            client.cookies.set("session_id", session_id)

            # Logout
            logout_response = await client.post("/logout")
            assert logout_response.status_code == 200

            # Verify session is deleted
            assert await redis_client.exists(f"session:{session_id}") == 0

            # Try to logout again (should fail)
            second_logout = await client.post("/logout")
            assert second_logout.status_code == 401

    async def test_concurrent_logins_different_users(
        self, app, mongo_manager, redis_client
    ):
        """Test multiple users logging in concurrently."""
        # Create multiple users
        users_data = []
        for i in range(3):
            password = f"password_{i}"
            user_doc = User(
                username=f"user_{i}",
                password=sha256(password.encode()).hexdigest(),
                role="admin",
                new_user=False,
                permissions=Permissions(
                    ledger=Ledger(read=True, write=True),
                    apd=AdvanceProvisionDemand(read=True, write=True),
                    overhaul_scale=OverhaulScale(read=True, write=True),
                    recieve_voucher=RecieveVoucher(read=True, write=True),
                    issue_voucher=IssueVoucher(read=True, write=True),
                    local_purchase_indent=LocalPurhcaseIndent(read=True, write=True),
                    local_purchase_quotation=LocalPurchaseQuotation(
                        read=True, write=True
                    ),
                    local_purchase_ordinance=LocalPurchaseOrdinance(
                        read=True, write=True
                    ),
                    local_purchase_pay=LocalPurchasePay(read=True, write=True),
                    local_purchase_query=LocalPurchaseQuery(read=True, write=True),
                    local_purchase_recieved=LocalPurchaseRecieved(
                        read=True, write=True
                    ),
                    local_purchase_ammend=LocalPurchaseAmmend(read=True, write=True),
                ),
            ).model_dump()
            users_data.append((user_doc, password))
            await mongo_manager.users.insert_one(user_doc)

        # Login all users
        sessions = []
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            for user_doc, password in users_data:
                response = await client.post(
                    "/login",
                    json={"username": user_doc["username"], "password": password},
                )
                assert response.status_code == 200
                sessions.append(extract_session_id(response))

        # Verify all sessions exist
        for session_id in sessions:
            assert await redis_client.exists(f"session:{session_id}") == 1

        # All session IDs should be unique
        assert len(sessions) == len(set(sessions))

        # Cleanup
        for session_id in sessions:
            await redis_client.delete(f"session:{session_id}")

    async def test_login_after_logout(
        self, app, mock_user, redis_client, valid_credentials
    ):
        """Test that user can login again after logout."""
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # First login
            login1 = await client.post("/login", json=valid_credentials)
            assert login1.status_code == 200
            session_id1 = extract_session_id(login1)

            # Set cookies and logout
            client.cookies.set("session_id", session_id1)
            logout = await client.post("/logout")
            assert logout.status_code == 200

            # Login again
            login2 = await client.post("/login", json=valid_credentials)
            assert login2.status_code == 200
            session_id2 = extract_session_id(login2)

            # Should get a new session ID
            assert session_id1 != session_id2

            # Old session should not exist
            assert await redis_client.exists(f"session:{session_id1}") == 0

            # New session should exist
            assert await redis_client.exists(f"session:{session_id2}") == 1

            # Cleanup
            await redis_client.delete(f"session:{session_id2}")
