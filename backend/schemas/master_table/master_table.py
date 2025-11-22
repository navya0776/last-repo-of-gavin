from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
# # ===== Enum =====
# class HeadEnum(str, Enum):
#     MT = "MT"
#     ENGR = "ENGR"
#     ORD = "ORD"
#     ACSF = "ACSF"
#     INDG_ARMT = "INDG ARMT"
#     INDA_INDGVEH = "INDA_INDG/VEH"
#     INDE = "INDE"


# ===== Base Schema =====
class MasterTableBase(BaseModel):
    Ledger_code: str = Field(..., max_length=4)
    eqpt_code: str = Field(..., max_length=4)
    eqpt_name: str = Field(..., max_length=50)
    ledger_name: str = Field(..., max_length=11)


# ===== Create Schema =====
class MasterTableCreate(MasterTableBase):
    pass


# ===== Update Schema =====
class MasterTableUpdate(BaseModel):
    eqpt_code: Optional[str] = Field(None, max_length=4)
    eqpt_name: Optional[str] = Field(None, max_length=50)
    ledger_name: Optional[str] = Field(None, max_length=11)


# ===== Response Schema =====
class MasterTableOut(MasterTableBase):
    model_config = ConfigDict(from_attributes=True)
