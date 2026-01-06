from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class LockRequest(BaseModel):
    key: str = Field(..., min_length=13)

    @field_validator("key")
    def validate_key(cls, v):
        if not any(c.islower() for c in v):
            raise ValueError("must contain lowercase")
        if not any(c.isupper() for c in v):
            raise ValueError("must contain uppercase")
        if not any(not c.isalnum() for c in v):
            raise ValueError("must contain a symbol")
        return v


class LockDetailsModel(BaseModel):
    date: datetime
    recieved_payment: bool
