from typing import List, Optional
from pydantic import BaseModel, field_validator, Field
from datetime import date

class Demand_Details(BaseModel):
    page_number:str #map from ledger 
    curr_stk_bal:int#
    dues_in:int#
    outs_reqd:int#
    stk_n_yr:int#
    reqd_as_OHS:int#
    cons_pattern_qty_eq:str#
    reqd_as_per_cons:int#
    qty_dem:int#
    recd:int#
    depot_control: str#
    depot_control_dt: str#
    d_e_l: Optional[bool]=None
    sub_dem_no:int

class AP_Demand(BaseModel):
    demand_number: int  # Must field
    demand_date: str = Field(default_factory=lambda: AP_Demand.get_today_date())  # auto today's date in string
    demand_type: str
    equipment_code: int
    equipment: str
    financial_year: str = Field(default_factory=lambda: AP_Demand.get_financial_year())
    number_of_equiment: int
    total_demand: int
    full_recieved: int
    partial_recieved: int
    outstanding: int
    percentage_recieved: int
    select: Optional[bool] = None

    @field_validator("equipment", "equipment_code", mode="before")
    def strip_strings(cls, value):
        """Strip extra spaces from string fields (safe for int as well)."""
        if isinstance(value, str):
            return value.strip()
        return value

    @staticmethod
    def get_today_date() -> str:
        """Return today's date in dd-mm-yyyy format."""
        return date.today().strftime("%d-%m-%Y")

    @staticmethod
    def get_financial_year() -> str:
        """Compute the financial year based on today's date (April–March)."""
        today = date.today()
        year = today.year
        # Indian-style FY: starts in April
        if today.month < 4:
            return f"{year - 1}-{year}"
        return f"{year}-{year + 1}"