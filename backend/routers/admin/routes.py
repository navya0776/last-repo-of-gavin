from core.middleware import get_admin_user
from fastapi import APIRouter, Depends, HTTPException, status
from repositories import LogsCollection, UserCollection
from schemas.admin import CreateUserRequest, LogFetchRequest, LogResponse

from data.models.users import User

# -----------------------------------------------------------------------------
# Admin Router
# -----------------------------------------------------------------------------
# This router contains routes accessible only to the administrator.
# The 'get_admin_user' dependency ensures that only authenticated admin users
# can access these endpoints.
# -----------------------------------------------------------------------------
router = APIRouter(dependencies=[Depends(get_admin_user)])


# -----------------------------------------------------------------------------
# Endpoint: Fetch Logs
# -----------------------------------------------------------------------------
@router.post("/logs/", response_model=tuple[LogResponse])
async def return_logs(logs: LogFetchRequest, logs_collection: LogsCollection):
    """
    Fetch a list of system logs, optionally filtered by username.

    Args:
        logs (LogFetchRequest): Parameters for fetching logs, including:
            - username: Optional username to filter logs by user.
            - start: Starting index (offset).
            - end: Ending index (exclusive upper bound).
        logs_collection (LogsCollection): MongoDB collection handler for logs.

    Returns:
        tuple[LogResponse]: A tuple of log entries sorted by newest first.

    Behavior:
        - If `username` is provided, filters logs by that user.
        - Otherwise, returns logs for all users.
        - Uses skip/limit for pagination.
        - Sorts logs in descending order by `_id` (newest first).
    """
    # Build query based on username (empty dict means match all)
    query = {"username": logs.username} if logs.username else {}

    # Calculate pagination
    skip = logs.start
    limit = logs.end - logs.start

    # Fetch results in descending order
    cursor = logs_collection.find(query).sort("_id", -1).skip(skip).limit(limit)

    # Convert MongoDB documents to Pydantic models
    return (LogResponse(**audits) async for audits in cursor)


# -----------------------------------------------------------------------------
# Endpoint: Fetch User Details
# -----------------------------------------------------------------------------
@router.post("/users/{username}", response_model=tuple[User])
async def return_user_detail(username: str | None, user_collection: UserCollection):
    """
    Retrieve details for a specific user or all users if username is None.

    Args:
        username (str | None): Username of the user to fetch.
        user_collection (UserCollection): MongoDB collection handler for users.

    Returns:
        tuple[User]: Tuple of user(s) converted to Pydantic models.

    Raises:
        HTTPException(404): If the requested user does not exist.

    Notes:
        - If a username is provided, fetches a single user document.
        - If username is None, returns all users.
    """
    if username is None:
        # Fetch a specific user by username
        user_doc = await user_collection.find_one({"username": username})

        if user_doc is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
            )

        user_model = (User(**user_doc),)
    else:
        # If no username provided, fetch all users
        user_doc = user_collection.find({})
        user_model = (User(**user) async for user in user_doc)

    return user_model


# -----------------------------------------------------------------------------
# Endpoint: Create New User
# -----------------------------------------------------------------------------
@router.post("/user")
async def create_user(
    user_creation_request: CreateUserRequest, user_collection: UserCollection
):
    """
    Create a new user in the database.

    Steps:
        1. Check if a user with the same username already exists.
        2. If the username is taken, raise an HTTP 400 error.
        3. Otherwise, insert the new user record into the collection.

    Args:
        user_creation_request (CreateUserRequest): Incoming user data (validated via Pydantic model).
        user_collection (UserCollection): The MongoDB collection handler for users.

    Raises:
        HTTPException: If a user with the provided username already exists.

    Returns:
        Status: 201
    """
    exists = await user_collection.find_one(
        {"username": user_creation_request.username}
    )

    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists!"
        )

    await user_collection.insert_one(user_creation_request.model_dump())
    return status.HTTP_201_CREATED


# -----------------------------------------------------------------------------
# Endpoint: Delete User
# -----------------------------------------------------------------------------
@router.delete("/user/{username:str}")
async def delete_user(username: str, user_collection: UserCollection):
    """
    Delete a user from the system.

    Args:
        username (str): The username of the user to delete.
        user_collection (UserCollection): MongoDB users collection handler.

    Returns:
        dict: Confirmation message upon successful deletion.

    Raises:
        HTTPException(404): If the user does not exist.
        HTTPException(500): If deletion fails unexpectedly.

    Behavior:
        - Verifies the user exists before deleting.
        - Deletes by username.
        - Returns a success message if deletion is confirmed.
    """
    # Verify user existence
    user = await user_collection.find_one({"username": username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{username}' not found!",
        )

    # Attempt deletion
    result = await user_collection.delete_one({"username": username})

    # Check deletion success
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user '{username}'.",
        )

    return {"message": f"User '{username}' deleted successfully."}
