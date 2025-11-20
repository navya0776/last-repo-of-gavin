from fastapi import APIRouter

from .cds_table import router as cds_router
from .master_table import router as master_table_router

router = APIRouter()

router.include_router(cds_router)
router.include_router(master_table_router, prefix="/master-table")

__all__ = ["router"]
