from typing import List

from pydantic import BaseModel, ConfigDict

# ======== Stock Analysis (API only) ========


class StockCategoryBreakdown(BaseModel):
    """Breakdown of one category, e.g. M/S/C or V/E/D."""

    total_qty: int
    unsv_stk: int
    rep_stk: int
    ser_stk: int
    per_stk: float
    D_in: int
    tot_stk: int
    per_tot_stk: int
    re_ord_lvl: int
    safety_stk: int
    zero_stk: int
    stk_less_than_2: int
    stk_less_than_5: int
    stk_less_than_10: int


class StockAnalysisResult(BaseModel):
    """Top-level structure for one ledger's computed stock analysis."""

    no_of_items: StockCategoryBreakdown
    scl_itms: StockCategoryBreakdown
    nsc_itms: StockCategoryBreakdown
    ved: StockCategoryBreakdown
    vital: StockCategoryBreakdown
    essential: StockCategoryBreakdown
    desirable: StockCategoryBreakdown
    msc: StockCategoryBreakdown
    mst_chng: StockCategoryBreakdown
    cld_chng: StockCategoryBreakdown
    shld_chng: StockCategoryBreakdown

    model_config = ConfigDict(from_attributes=True)
