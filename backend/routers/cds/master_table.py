"""from fastapi import APIRouter, Depends, HTTPException
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
#    GET /cds/master/list"""
# ====================================================
"""@router.get("/list", response_model=list[AddEquipmentView])
async def get_master_table(
    perms: UserPermissions,
    db: AsyncSession = Depends(get_db)
):
    if not perms.ledger.read:
        raise HTTPException(status_code=403, detail="Permission denied")

    stmt = select(MasterTable)
    result = await db.scalars(stmt)
    return result.all()"""

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
"""@router.get("/list", response_model=list[CDSView_primary])
async def list_all_equipment(
    perms: UserPermissions,
    session: AsyncSession = Depends(get_db)
):
    if not perms.ledger.read:
        raise HTTPException(status_code=403, detail="Not allowed to read CDS")

    stmt = select(
        cds_table.ledger_code,
        cds_table.eqpt_code,
        cds_table.equipment_name.label("eqpt_name"),
        cds_table.grp,
        cds_table.head,
        cds_table.db.label("Database")
    )

    result = await session.execute(stmt)
    rows = result.mappings().all()   # <-- IMPORTANT

    return rows"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.utils.users import UserPermissions
from data.database import get_db
from data.models.master_tbl import MasterTable

router = APIRouter(
    prefix="/cds",
    tags=["Master Table"]
)

# ============================================================
#  FETCH LIST FROM MASTER TABLE (Dropdown List for Add Eqpt)
# ============================================================
@router.get("/master-list")
async def fetch_master_table_list(
    perms: UserPermissions,
    session: AsyncSession = Depends(get_db)
):
    # Permission: user must have read access to ledger
    if not perms.ledger.read:
        raise HTTPException(status_code=403, detail="Not allowed to read master table")

    stmt = select(
        MasterTable.Ledger_code.label("ledger_code"),
        MasterTable.eqpt_code.label("eqpt_code"),
        MasterTable.ledger_name.label("ledger_name"),
        MasterTable.head.label("head")
    )

    result = await session.execute(stmt)
    rows = result.mappings().all()

    return rows