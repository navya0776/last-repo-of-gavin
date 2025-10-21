from pydantic import BaseModel, Field
from typing import List, Optional


class Details(BaseModel):
    sub_demand_number : int
    ledger_page_number: str
    ohs_number: Optional[int] = None
    isg_number: Optional[int] = None
    ssg_number: Optional[int] = None
    part_number: int
    nomenclature: str
    A_U : str
    auth : int
    current_stock_balance : int
    dues_in : int
    outstanding_requested : int
    stock_n_yr : int #iska sahi name nhi mila, correct it when u find the right name.
    requested_as_ohs : int
    consumption_pattern : str #qty/eqpt
    requested_as_per_consumption : int
    quantity_demanded : int
    recieved : int
    depot_control : str
    depot_control_dt : str
    d_e_l : str



class Demand(BaseModel):
    demand_number : int
    demand_type : str
    equipment_code : int
    equipment : str
    financial_year : str
    number_of_equiment : int
    total_demand : int
    full_recieved : int
    partial_recieved : int
    outstanding : int
    percentage_recieved : int
    details : List[Details]
