from pydantic import BaseModel, model_validator, ConfigDict

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
    #test
    model_config = ConfigDict(from_attributes=True)  # ✅ tells Pydantic it's an ORM
    #test

    @model_validator(mode="after")
    def validate_fields(self):
        """Perform general validation for username and password."""
        if " " in self.username:
            raise ValueError("Username must not contain spaces")
        if " " in self.password:
            raise ValueError("Password must not contain spaces")

        return self
