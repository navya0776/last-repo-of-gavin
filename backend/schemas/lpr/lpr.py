from pydantic import BaseModel, field_validator
from typing import Optional

# ================================
# BASE SCHEMA
# ================================
class LPRBase(BaseModel):
    job_no: int
    srl: Optional[int] = None
    scale: Optional[str] = None
    part_no: Optional[str] = None
    nomenclature: Optional[str] = None
    au: Optional[str] = None
    qty: Optional[int] = None

    @field_validator("*", mode="before")
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


# ================================
# CREATE SCHEMA
# ================================
class LPRCreate(LPRBase):
    lpr_no: int   # PK included (your requirement)


# ================================
# RESPONSE SCHEMA
# ================================
class LPRResponse(LPRBase):
    lpr_no: int

    class Config:
        from_attributes = True
