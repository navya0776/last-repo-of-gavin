from pydantic import BaseModel, Field, field_validator
from typing import Optional
from .permissions import Permissions


class User(BaseModel):
    """
    Model for storing user accounts with validation.
    Typically used in the 'users' collection.
    """

    username: str = Field(..., min_length=3, max_length=30, description="Unique username for login")
    password: str = Field(..., min_length=5, description="Password (will be hashed before storage)")
    new_user: bool = Field(default=True, description="Flag indicating if this is a new user")
    role: str = Field(..., description="User role — e.g., admin, manager, viewer")
    permissions: Permissions = Field(..., description="Permission set for this user")

    # ✅ Username validator
       # ✅ Username validator (no spaces)
    @field_validator("username")
    def validate_username(cls, v):
        if " " in v:
            raise ValueError("Username must not contain spaces")
        return v.strip().lower()  # normalize

    # ✅ Password validator (no spaces)
    @field_validator("password")
    def validate_password(cls, v):
        if " " in v:
            raise ValueError("Password must not contain spaces")
        return v.strip()
    def validate_password_length(cls, v):
        if len(v) < 5:
            raise ValueError("Password must be at least 8 characters long")