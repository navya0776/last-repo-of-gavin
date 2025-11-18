from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List

# ===== Enum =====
class HeadEnum(str, Enum):
    MT = "MT"
    ENGR = "ENGR"
    ORD = "ORD"
    ACSF = "ACSF"
    INDG_ARMT = "INDG ARMT"
    INDA_INDGVEH = "INDA_INDG/VEH"
    INDE = "INDE"


# ===== Base Schema =====
class MasterTableBase(BaseModel):
    Ledger_code: str = Field(..., max_length=4)
    eqpt_code: str = Field(..., max_length=4)
    eqpt_name: str = Field(..., max_length=11)
    head: HeadEnum


# ===== Create Schema =====
class MasterTableCreate(MasterTableBase):
    pass


# ===== Update Schema =====
class MasterTableUpdate(BaseModel):
    eqpt_code: Optional[str] = Field(None, max_length=4)
    eqpt_name: Optional[str] = Field(None, max_length=11)
    head: Optional[HeadEnum] = None


# ===== Response Schema =====
class MasterTableOut(MasterTableBase):
    class Config:
        from_attributes = True  # Enables ORM model compatibility
