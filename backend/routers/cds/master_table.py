from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.utils.users import UserPermissions

from data.database import get_db
from data.models.master_tbl import MasterTable

router = APIRouter(prefix="/cds", tags=["Master Table"])


# ============================================================
#  FETCH LIST FROM MASTER TABLE (Dropdown List for Add Eqpt)
# ============================================================
@router.get("/master-list")
async def fetch_master_table_list(
    perms: UserPermissions, session: AsyncSession = Depends(get_db)
):
    # Permission: user must have read access to ledger
    if not perms.ledger.read:
        raise HTTPException(status_code=403, detail="Not allowed to read master table")

    stmt = select(
        MasterTable.Ledger_code.label("ledger_code"),
        MasterTable.eqpt_code.label("eqpt_code"),
        MasterTable.ledger_name.label("ledger_name"),
        MasterTable.head.label("head"),
    )

    result = await session.execute(stmt)
    rows = result.mappings().all()

    return rows

