import re
from datetime import date
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ConfigDict


# ============================================================
# ENUM
# ============================================================
class DemandTypeEnum(str, Enum):
    APD = "APD"
    SPD = "SPD"


# ============================================================
# DMD JUNCTION SCHEMAS
# ============================================================
class DmdJunctionBase(BaseModel):
    Page_no: str = Field(..., max_length=20)
    demand_no: int
    is_locked: bool

    Scale_no: str = Field(..., max_length=10)
    Part_no: str = Field(..., max_length=10)
    Nomenclature: str = Field(..., max_length=10)
    A_u: str = Field(..., max_length=10)
    Auth: int = Field(..., ge=0)
    Curr_stk_bal: int = Field(..., ge=0)
    Dues_in: int = Field(..., ge=0)
    Outs_Reqd: int = Field(..., ge=0)

    stk_N_yr: int = Field(0, ge=0)
    Reqd_as_OHS: int = Field(0, ge=0)
    Cons_pattern: str = Field("0/0")
    qty_dem: int = Field(0, ge=0)
    Recd: int = Field(0, ge=0)

    Dept_ctrl: str = Field("0", max_length=10)
    Dept_ctrl_dt: Optional[str] = None

    @field_validator("Cons_pattern")
    def validate_pattern(cls, v):
        if not re.match(r"^\d+/\d+$", v):
            raise ValueError("Cons_pattern must be in 'X/Y' format.")
        return v

    @field_validator("Recd")
    def recd_cannot_exceed_demand(cls, v, values):
        if "qty_dem" in values and v > values["qty_dem"]:
            raise ValueError("Received quantity cannot exceed demanded quantity.")
        return v


class DmdJunctionCreate(DmdJunctionBase):
    eqpt_code: str


class DmdJunctionResponse(DmdJunctionBase):
    model_config = ConfigDict(from_attributes=True)


# ============================================================
# DEMAND RESPONSE (FOR LIST & DETAIL)
# ============================================================
class DemandResponse(BaseModel):
    demand_no: int
    eqpt_code: str
    eqpt_name: str
    fin_year: str = Field(..., pattern=r"^\d{4}-\d{4}$")
    demand_type: DemandTypeEnum

    demand_auth: Optional[str]
    full_received: int
    part_received: int
    outstanding: int
    percent_received: float

    # UI: "No Eqpt" = no_of_apd_demand_placed
    no_eqpt: int = Field(..., alias="no_of_apd_demand_placed")

    @field_validator("fin_year")
    def ensure_fin_year_span_is_1(cls, v):
        start, end = map(int, v.split("-"))
        if end - start != 1:
            raise ValueError("fin_year must span exactly one year (2024-2025)")
        return v

    model_config = ConfigDict(
        from_attributes=True, validate_by_alias=True, validate_by_name=True
    )


# ============================================================
# DEMAND CREATE (FULL FORM)
# ============================================================
class DemandCreate(BaseModel):
    # Required fields
    eqpt_code: str
    eqpt_name: str
    fin_year: str = Field(..., pattern=r"^\d{4}-\d{4}$")
    demand_type: DemandTypeEnum

    # UI "No of eqpt demand placed"
    no_of_apd_demand_placed: Optional[int] = 0

    # Optional fields from ORM
    demand_auth: Optional[str] = None
    remarks: Optional[str] = None

    store_code: Optional[str] = None
    make: Optional[str] = None
    scale_or_ssg_ref: Optional[str] = None

    ap_demand_date_from: Optional[date] = None
    ap_demand_date_to: Optional[date] = None

    consumption_pattern_from: Optional[date] = None
    consumption_pattern_to: Optional[date] = None

    demand_range_from: Optional[int] = None
    demand_range_to: Optional[int] = None

    no_of_apd_completed: Optional[int] = 0
    no_of_eopt_for_spares: Optional[int] = 0
    no_of_eopt_outs_for_repair: Optional[int] = 0

    depot: Optional[str] = None
    city: Optional[str] = None
    prefix: Optional[str] = None

    oh_scale_ssg: Optional[bool] = False
    demand_index_ledger_page: Optional[bool] = False
    demand_index_oh_scale: Optional[bool] = False
    demand_index_demand_no: Optional[bool] = False

    is_adv_prov_demand: Optional[bool] = False
    is_supplementary_demand: Optional[bool] = False

    is_all_scaled_items: Optional[bool] = False
    is_on_selection: Optional[bool] = False

    ahq_sr: Optional[str] = None
    section: Optional[str] = None
    ledger_code: Optional[str] = None
    ledger_name: Optional[str] = None

    date_of_issue: Optional[date] = None
    scale_issue_no: Optional[str] = None

    # nested spares rows
    dmd_details: Optional[List[DmdJunctionCreate]] = None

    @field_validator("fin_year")
    def ensure_fin_year_span_is_1(cls, v):
        start, end = map(int, v.split("-"))
        if end - start != 1:
            raise ValueError("fin_year must span exactly one year (ex: 2024-2025)")
        return v


class EquiptmentResponse(BaseModel):
    eqpt_code: str
    equipment_name: str

    model_config = ConfigDict(from_attributes=True)
