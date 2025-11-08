from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime


class AuthSignatoryBase(BaseModel):
    document: str = Field(
        ..., description="Document type or name the signatory is associated with"
    )
    name: Optional[str] = Field(None, description="Name of the authorized signatory")
    rank: Optional[str] = Field(
        None, description="Rank or level of the signatory (can be predefined in future)"
    )
    designation: Optional[str] = Field(
        None, description="Official designation or title"
    )
    signed_for: str = Field(
        ..., description="Entity or purpose for which the document is signed"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp when record created"
    )

    @field_validator("document", "signed_for")
    def must_not_be_empty(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.name} cannot be empty")
        return v


class AuthSignatoryCreate(AuthSignatoryBase):
    pass


class AuthSignatoryResponse(AuthSignatoryBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
