from typing import Literal
from pydantic import BaseModel

# ======= Store =========
class StoreBase(BaseModel):
    store_name: str
    store_id: int

class StoreResponse(StoreBase):
    pass

#======== Ledger ========
class LedgerBase(BaseModel):
    Ledger_name: str
    Ledger_code: int

class LedgerCreate(LedgerBase):
    @model_validator(mode="after")
    def check_class(self):
        if not self.Ledger_name and not self.Ledger_code:
            raise ValueError("Fields cannot be empty")
        return self

class LedgerResponse(LedgerBase):
    pass

    class Config:
        orm_mode = True

#======== LedgerMaint ========
class LedgerMaintenance(BaseModel):
    ledger_page: str
    ohs_number: str | None = None
    isg_number: str | None = None
    ssg_number: str | None = None
    part_number: str
    nomenclature: str
    a_u: str
    no_off: int
    scl_auth: int
    unsv_stock: int
    rep_stock: int
    serv_stock: int
    msc: Literal["M", "S", "C"]
    ved: Literal["V", "E", "D"]
    in_house: Literal["in_house", "ORD"]
    dues_in: int | None = None
    consumption: int | None = None
    bin_number: str | None = None
    group: str | None = None

class LedgerMaintanenceCreate(LedgerMaintenanceBase):
    cos_sec: str #add in ORM of LedgerMaintenance
    cab_no: str
    old_pg_ref: float
    Assy_Comp: str
    Re_ord_lvl: int
    safety_stk: int

    @model_validator(mode="after")
    def bulk_validate(self):
        skip_fields = {"consumption", "serv_stock","rep_stock","unsv_stock", "scl_auth", "no_off", "a_u", "nomenclature","ohs_no","bin_number", "group", "part_number"}
        for name, value in self.model_dump().items():
            if name in skip_fields:
                continue
            # Example generic rule: integers must be non-negative
            if isinstance(value, int) and value < 0:
                raise ValueError(f"{name} must be >= 0")
            # Example generic rule: strings trimmed and non-empty
            if isinstance(value, str) and not value.strip():
                raise ValueError(f"{name} cannot be empty")
        return self


class LedgerMaintanenceUpdate(LedgerMaintenanceBase):
    cos_sec: str #add in ORM of LedgerMaintenance
    cab_no: str
    old_pg_ref: float
    Assy_Comp: str
    Re_ord_lvl: int
    safety_stk: int

    @model_validator(mode="after")
    def bulk_validate(self):
        skip_fields = {"consumption", "serv_stock","rep_stock","unsv_stock", "scl_auth", "no_off", "a_u", "nomenclature","ohs_no","bin_number", "group", "part_number"}
        for name, value in self.model_dump().items():
            if name in skip_fields:
                continue
            # Example generic rule: integers must be non-negative
            if isinstance(value, int) and value < 0:
                raise ValueError(f"{name} must be >= 0")
            # Example generic rule: strings trimmed and non-empty
            if isinstance(value, str) and not value.strip():
                raise ValueError(f"{name} cannot be empty")
        return self

class LedgerMaintenanceResponse(LedgerMaintenanceBase):
    cds_unsv_stock: int
    cds_rep_stock: int
    cds_serv_stock: int
    lpp: str | None = None
    rate: float
    rmks: str
    lpp_dt: str

    class Config:
        orm_mode = True
