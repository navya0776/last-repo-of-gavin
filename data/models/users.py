from pydantic import BaseModel

from .permissions import Permissions


class User(BaseModel):
    """
    Collection model for storing all user accounts.
    This will likely be your 'users' collection.
    """

    username: str
    password: str
    new_user: bool
    role: str
    permissions: Permissions
