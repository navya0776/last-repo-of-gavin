from typing import List
from pydantic import BaseModel, ConfigDict


# ======== Stock Analysis (API only) ========


class StockCategoryBreakdown(BaseModel):
    """Breakdown of one category, e.g. M/S/C or V/E/D."""

    demand: int
    full_recd: int
    pt_recd: int
    outs: int
    per_recd: float
    deleted: int
    in_iil: int
    in_cvil: int
    critical: int
    ctrl_no_na: int


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

