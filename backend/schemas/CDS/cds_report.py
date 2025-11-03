from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# ============================================================
# 🧩 Base Schema — shared fields (used internally or for inheritance)
# ============================================================

class CDSReportBase(BaseModel):
    srl:int
    ledger_code:str
    scale:str
    part_no:int
    nomenclature:str
    a_u:str
    per_assy:int
    job:Optional[int]=None
    total:int
    group:str
    
class CDSDemandResponse(CDSReportBase):
    pass
    model_config = ConfigDict(from_attributes=True)