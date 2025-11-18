from datetime import date
from typing import Optional
from pydantic import ConfigDict, field_validator, Field
from ..Basemodel import (
    CDSBase_primary, AddEquipmentBase, JobMasterBase, CDSBase_secondary,
)

# ========= CDS primary ==========


class CDSView_primary(CDSBase_primary):
    pass
    model_config = ConfigDict(from_attributes=True)

# ========= Add Equipment ==========


class AddEquipmentCreate(AddEquipmentBase):
    grp: str = Field(..., min_length=4,
                     description="""
                     Group is the name of the equipment group and must be at
                     least 4 characters long""")

    head: str = Field(..., min_length=4,
                      description="Head must be at least 4 characters long")

    equipment_name: str = Field(..., min_length=4)

    @field_validator("*", mode="before")
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("equipment_name", "grp", mode="before")
    def strip_specific_fields(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class AddEquipmentView(AddEquipmentBase):
    ledger_name: str

    model_config = ConfigDict(from_attributes=True)

# ========= JobMaster ==========


class JobMasterCreate(JobMasterBase):
    eqpt_code: str = Field(...)
    Rmks: Optional[str] = None
    job_prefix: Optional[str] = None
    nature_rep: str = Field(...)
    Depot: str
    date_recd: date

    @field_validator("*", mode="before")
    def clean_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class JobMasterView(JobMasterBase):

    eqpt_code: str
    Rmks: Optional[str] = None
    no_comp: Optional[int] = None
    date_comp: Optional[date] = None
    item_dem: Optional[int] = None
    full_iss: Optional[int] = None
    part_iss: Optional[int] = None
    nil_iss: Optional[int] = None
    bal_itens: int
    cancel_nr: Optional[int] = None
    on_LPR: Optional[int] = None
    enq_placed: Optional[int] = None
    SO_placed: Optional[int] = None
    recd_full: Optional[int] = None
    recd_part: Optional[int] = None
    cancel_prog: Optional[int] = None
    mt_lp: Optional[int] = None
    engr_lp: int
    ord_lp: Optional[int] = None
    total_lp: int
    LP_access_date: date
    comit_type: Optional[str] = None
    vir1: Optional[int] = None
    vir_dt1: Optional[int] = None
    vir_dem1: Optional[int] = None
    vir_iss1: Optional[int] = None
    vir2: Optional[int] = None
    vit_dt2: Optional[int] = None
    vir_dem2: Optional[int] = None
    vir_iss2: Optional[int] = None
    vir_3: Optional[int] = None
    vir_dt3: Optional[int] = None
    vir_dem3: Optional[int] = None
    vir_iss3: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class AddDemandView(JobMasterBase):
    pass


# ========= CDS Secondry ==========


class CDSView_demand(CDSBase_secondary):
    pass


class CdsView(CDSBase_secondary):
    job_no: int
    job_date: date
    ledger_page: str
    ohs_no: Optional[int] = None
    part_number: Optional[str] = None
    spart_no: Optional[str] = None
    nomenclature: Optional[str] = None
    auth_officer: Optional[str] = None
    dem_ref_no: Optional[int] = None
    add_dem_no: Optional[int] = None
    lpr_qty: Optional[int] = None
    lpr_no: Optional[str] = None
    lpr_date: Optional[date] = None
    demand_ctrl_no: Optional[str] = None
    demand_ctrl_date: Optional[date] = None
    curr_stock: Optional[int] = None
    now_issue_qty: Optional[int] = None
    recd_qty: Optional[int] = None
    date_nr: Optional[date] = None
    oss_qty1: Optional[int] = None
    oss_iv1: Optional[str] = None
    oss_ivdt1: Optional[date] = None
    oss_qty2: Optional[int] = None
    oss_iv2: Optional[str] = None
    oss_ivdt2: Optional[date] = None
    oss_qty3: Optional[int] = None
    oss_iv3: Optional[str] = None
    oss_ivdt3: Optional[date] = None
    cds_iv1: Optional[str] = None
    cds_ivdt1: Optional[date] = None
    cds_qty2: Optional[int] = None
    cds_iv2: Optional[str] = None
    cds_ivdt2: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)
