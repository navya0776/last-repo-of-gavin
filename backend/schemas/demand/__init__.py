import re
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from enum import Enum


# ENUM
class DemandTypeEnum(str, Enum):
    APD = "APD"
    SPD = "SPD"


#       DMD JUNCTION SCHEMA
class DmdJunctionBase(BaseModel):
    Page_no: str = Field(..., max_length=20, description="Ledger page reference")
    demand_no: int = Field(..., description="Foreign key to Demand table")
    is_locked: bool = Field(..., description="Whether this row is locked")

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
    Cons_pattern: str = Field("0/0", description="Format X/Y")
    qty_dem: int = Field(0, ge=0)
    Recd: int = Field(0, ge=0)

    Dept_ctrl: str = Field("0", max_length=10)
    Dept_ctrl_dt: Optional[str] = Field(None, description="Date of department control")

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


class DemandResponse(BaseModel):
    demand_no: int
    eqpt_code: str
    equipment: str = Field(..., max_length=11)
    no_equipment: int

    fin_year: str = Field(
        ...,
        pattern=r"^\d{4}-\d{4}$",
        description="Format YYYY-YYYY (Auto-generated for April cycle)",
    )

    demand_type: DemandTypeEnum
    demand_auth: int
    full_received: int = Field(0, ge=0)
    part_received: int = Field(0, ge=0)
    outstanding: int = Field(0, ge=0)
    percent_received: float = Field(0.0, ge=0, le=100)

    @field_validator("fin_year")
    def ensure_fin_year_span_is_1(cls, v):
        start, end = map(int, v.split("-"))
        if end - start != 1:
            raise ValueError("fin_year must be a 1-year span (e.g., 2024-2025)")
        return v

    model_config = ConfigDict(from_attributes=True)
