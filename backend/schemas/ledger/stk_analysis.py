from typing import Dict, List
from pydantic import BaseModel, ConfigDict


# ======== Stock Analysis (API only) ========

class StockCategoryBreakdown(BaseModel):
    """Breakdown of one category, e.g. M/S/C or V/E/D."""
    total_qty:int
    unsv_stk:int
    rep_stk:int
    ser_stk:int
    per_stk:float
    D_in:int
    tot_stk:int
    per_tot_stk:int
    re_ord_lvl:int
    safety_stk:int
    zero_stk:int
    stk_less_than_2:int
    stk_less_than_5:int
    stk_less_than_10:int



class StockAnalysisResult(BaseModel):
    """Top-level structure for one ledger's computed stock analysis."""
    no_of_items: List[StockCategoryBreakdown]
    scl_itms: List[StockCategoryBreakdown]
    nsc_itms: List[StockCategoryBreakdown]
    ved: List[StockCategoryBreakdown]
    vital: List[StockCategoryBreakdown]
    essential: List[StockCategoryBreakdown]
    desirable: List[StockCategoryBreakdown]
    msc: List[StockCategoryBreakdown]
    mst_chng: List[StockCategoryBreakdown]
    cld_chng: List[StockCategoryBreakdown]
    shld_chng: List[StockCategoryBreakdown]

    model_config = ConfigDict(from_attributes=True)