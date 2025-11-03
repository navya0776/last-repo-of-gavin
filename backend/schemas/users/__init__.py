from pydantic import BaseModel, model_validator

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

    @model_validator(mode="after")
    def validate_fields(self):
        """Perform general validation for username and password."""
        if " " in self.username:
            raise ValueError("Username must not contain spaces")
        if " " in self.password:
            raise ValueError("Password must not contain spaces")

        return self
