from pydantic import BaseModel
from typing import List, Optional

class control_demand(BaseModel):
    eqpt_name:str
    eqpt_code:str
    head:str
    eqpt_id:int
    ledger_id:int
    section:str

