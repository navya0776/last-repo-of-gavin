from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ControlDemandBase(BaseModel):
    eqpt_name: str = Field(..., description="Name of the equipment")
    eqpt_code: str = Field(..., description="Unique code of the equipment")
    head: str = Field(..., description="Head or department responsible")
    eqpt_id: int = Field(..., description="Unique equipment identifier")
    ledger_id: int = Field(..., description="Associated ledger ID")
    section: str = Field(..., description="Section or category of the equipment")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")

    # Validators to ensure critical fields are not empty
    @field_validator("eqpt_name", "eqpt_code", "head", "eqpt_id", "ledger_id","section")
    def no_empty_string(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.name} cannot be empty")
        return v

class ControlDemandCreate(ControlDemandBase):
    pass

class ControlDemandResponse(ControlDemandBase):
    id: int

    class Config:
        orm_mode = True
