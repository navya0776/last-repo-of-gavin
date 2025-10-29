from pydantic import BaseModel, model_validator
from typing import Any


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


class UserResponse(LogResponse):
    pass
