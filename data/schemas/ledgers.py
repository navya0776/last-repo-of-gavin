from typing import Literal
from pydantic import BaseModel

class AllStores(BaseModel):
    store_name: str
    store_id: str
    Ledger_name: List[Ledger_no]

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
    cds_unsv_stock: int
    cds_rep_stock: int
    cds_serv_stock: int
    lpp: str | None = None
