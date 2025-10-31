from pydantic import BaseModel
from typing import Optional
from datetime import date

class APDemandBase(BaseModel):
    demand_no: str
    demand_type: str  # "APD" or "SPD"
    equipment_code: str
    equipment_name: str
    fin_year: str
    demand_auth: Optional[str] = None
    depot: Optional[str] = None
    prefix: Optional[str] = None
    city: Optional[str] = None
    full_received: Optional[int] = 0
    part_received: Optional[int] = 0
    outstanding: Optional[int] = 0
    percent_received: Optional[float] = 0.0
    remarks: Optional[str] = None

class APDemandCreate(APDemandBase):
    pass

class APDemandUpdate(BaseModel):
    full_received: Optional[int] = None
    part_received: Optional[int] = None
    outstanding: Optional[int] = None
    percent_received: Optional[float] = None
    remarks: Optional[str] = None
