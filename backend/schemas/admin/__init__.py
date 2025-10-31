from typing import Any

from pydantic import BaseModel, model_validator

from data.models.users import User


class LogFetchRequest(BaseModel):
    username: str | None
    start: int
    end: int

    @model_validator(mode="after")
    def validate_range(self):
        if self.start == self.end:
            raise ValueError("Start and end cannot be equal")
        if self.start > self.end:
            raise ValueError("Start must be less than end")
        if self.start < 0 or self.end < 0:
            raise ValueError("Start or end must be greater than user ")
        if self.end - self.start > 100:
            raise ValueError("Too many logs to query")
        return self


class LogResponse(BaseModel):
    username: str | None
    start: int
    end: int

    @model_validator(mode="before")
    def remove_mongo_id(cls, values: dict[str, Any]):
        # Drop MongoDB's internal _id key if present
        values.pop("_id", None)
        return values


class CreateUserRequest(User):
    new_user = True

    @model_validator(mode="after")
    def assert_role_is_not_admin(self):
        if self.role == "admin":
            raise ValueError("Only 1 admin can exist!")
        return self

    @model_validator(mode="after")
    def assert_new_user_is_true(self):
        if not self.new_user:
            raise ValueError("New User param must be true!")
        return self
