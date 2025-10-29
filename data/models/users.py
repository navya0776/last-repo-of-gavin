from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId


class RolePermissions(BaseModel):
    """
    Defines the specific permissions for a role.
    This structure ensures fine-grained control over user actions.
    """

    read: bool
    write: bool
    delete: bool


class Role(BaseModel):
    """
    Collection model for defining all available roles and their associated permissions.
    This will likely be a separate collection in your database (e.g., 'roles').
    """

    role_name: str
    permissions: RolePermissions


class User(BaseModel):
    """
    Collection model for storing all user accounts.
    This will likely be your 'users' collection.
    """

    id: str = Field(default_factory=lambda: str(ObjectId()))
    username: str
    password: str | bytes
    role: Role
