from datetime import date
from pydantic import BaseModel
from ..ledger.ledgers import LedgerMaintenanceBase

# ========= CDS primary ==========


class CDSBase_primary(BaseModel):
    equipment_name: str
    head: str
    eqpt_code: str
    ledger_code: str
    grp: str


# ========= Add Equipment ==========


class AddEquipmentBase(BaseModel):
    ledger_code: str
    eqpt_code: str


# ========= JobMaster ==========


class JobMasterBase(BaseModel):
    eqpt_name: str
    job_no: int
    job_date: date
    no_eqpt: int


# ========= CDS Secondry ==========


class CDSBase_secondary(BaseModel):
    demand_no: int
    demand_date: date


class Cds_dmd_Create(BaseModel):
    ledger_list: list[LedgerMaintenanceBase]
