from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class Demand_Details(BaseModel):
    ohs_number: int #
    part_number: int#
    nomenclature: str#
    a_u: str#
    scl_auth: int#
    page_number:str #
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
    d_e_l: Optional[bool]=None#
    sub_dem_no:int

class AP_Demand(BaseModel):
    #all must except select
    demand_number: int #Must field for validator 
    demand_date:date#must
    demand_type: str 
    equipment_code: int
    equipment: str
    financial_year: str
    number_of_equiment: int
    total_demand: int
    full_recieved: int
    partial_recieved: int
    outstanding: int
    percentage_recieved: int
    select:Optional[bool]=None
    details: list[Demand_Details]