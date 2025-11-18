from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from data.database import get_db
from data.models.master_tbl import MasterTable

from backend.schemas.CDS.cds import AddEquipmentCreate, AddEquipmentView
from backend.utils.users import UserPermissions


# MAIN PREFIX UPDATED ✔
router = APIRouter(
    prefix="/cds/master",
    tags=["Master Table"]
)


# ====================================================
# 1️⃣ GET MASTER TABLE LIST
#    GET /cds/master/list
# ====================================================
@router.get("/list", response_model=list[AddEquipmentView])
async def get_master_table(
    perms: UserPermissions,
    db: AsyncSession = Depends(get_db)
):
    if not perms.ledger.read:
        raise HTTPException(status_code=403, detail="Permission denied")

    stmt = select(MasterTable)
    result = await db.scalars(stmt)
    return result.all()

"""
# ====================================================
# 2️⃣ ADD NEW EQUIPMENT TO MASTER TABLE
#    POST /cds/master/add
# ====================================================
@router.post("/add", response_model=AddEquipmentView)
async def add_master_equipment(
    data: AddEquipmentCreate,
    perms: UserPermissions,
    db: AsyncSession = Depends(get_db)
):
    if not perms.ledger.write:
        raise HTTPException(status_code=403, detail="Permission denied")

    stmt = select(MasterTable).where(MasterTable.eqpt_code == data.eqpt_code)
    exists = await db.scalar(stmt)
    if exists:
        raise HTTPException(
            status_code=400,
            detail="Equipment with this eqpt_code already exists"
        )

    new_row = MasterTable(
        Ledger_code=data.ledger_code,
        eqpt_code=data.eqpt_code,
        ledger_name="",   # fill from UI
        head=""           # fill from UI
    )

    db.add(new_row)
    await db.commit()
    await db.refresh(new_row)

    return new_row"""