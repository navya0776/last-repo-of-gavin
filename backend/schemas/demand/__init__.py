import re
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
from enum import Enum
from datetime import datetime


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
    pass


class DmdJunctionResponse(DmdJunctionBase):
    model_config = ConfigDict(from_attributes=True)


class DemandBase(BaseModel):
    eqpt_code: str = Field(..., description="Foreign key to master_table.eqpt_code")
    demand_type: DemandTypeEnum = Field(..., description="APD / SPD")
    eqpt_name: str = Field(..., max_length=11)

    # Optional because it will auto-generate
    fin_year: Optional[str] = Field(
        None,
        pattern=r"^\d{4}-\d{4}$",
        description="Format YYYY-YYYY (Auto-generated for April cycle)",
    )

    demand_auth: Optional[str] = Field(None, max_length=100)
    full_received: int = Field(0, ge=0)
    part_received: int = Field(0, ge=0)
    outstanding: int = Field(0, ge=0)
    percent_received: float = Field(0.0, ge=0, le=100)
    remarks: Optional[str] = Field(None, max_length=255)

    # ➕ NEW FIELD: DEPOT
    depot: Optional[str] = Field(
        None, max_length=100, description="Depot responsible for demand processing"
    )

    dmd_details: Optional[List["DmdJunctionCreate"]] = Field(
        None, description="List of ledger junction rows"
    )

    # ---------------- VALIDATORS ----------------

    @field_validator("depot")
    def validate_depot(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError("Depot cannot be empty or whitespace.")
        return v

    @field_validator("fin_year", mode="before")
    def auto_generate_fin_year(cls, v):
        if v is not None:
            return v

        today = datetime.now()
        year = today.year
        month = today.month

        if month < 4:
            start_year = year - 1
            end_year = year
        else:
            start_year = year
            end_year = year + 1

        return f"{start_year}-{end_year}"

    @field_validator("fin_year")
    def ensure_fin_year_span_is_1(cls, v):
        start, end = map(int, v.split("-"))
        if end - start != 1:
            raise ValueError("fin_year must be a 1-year span (e.g., 2024-2025)")
        return v

    @field_validator("percent_received")
    def percent_must_match_values(cls, v, values):
        full = values.get("full_received", 0)
        part = values.get("part_received", 0)
        total = full + part
        if total > 0 and v == 0:
            raise ValueError("percent_received must reflect full+part received values.")
        return v


class DemandCreate(DemandBase):
    pass


class DemandResponse(DemandBase):
    demand_no: int = Field(..., description="Auto-increment primary key")
    model_config = ConfigDict(from_attributes=True)
