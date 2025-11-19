from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.schemas.CDS.cds import AddEquipmentCreate, AddEquipmentView,CDSView_primary
from backend.utils.users import UserPermissions
from data.database import get_db
from data.models.cds import cds_table
from data.models.master_tbl import MasterTable
router = APIRouter(
    prefix="/cds",
    tags=["CDS Table"]
)

# ============================================================
#  GET ALL ENTRIES FROM cds_table
# ============================================================
@router.get("/list", response_model=list[CDSView_primary])
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
    rows = result.mappings().all()

    return rows


# ============================================================
#  ADD EQUIPMENT ENTRY INTO cds_table
# ============================================================


@router.post("/add", response_model=CDSView_primary)
async def add_equipment(
    payload: AddEquipmentCreate,
    perms: UserPermissions,
    session: AsyncSession = Depends(get_db)
):
    if not perms.ledger.write:
        raise HTTPException(status_code=403, detail="Not allowed to write CDS")

    # -------------------------------------------------------
    # VALIDATE THAT eqpt_code + ledger_code EXIST IN MASTER TABLE
    # -------------------------------------------------------
    master_exists = await session.scalar(
        select(MasterTable).where(
            MasterTable.eqpt_code == payload.eqpt_code,
            MasterTable.Ledger_code == payload.ledger_code
        )
    )
    if not master_exists:
        raise HTTPException(
            status_code=400,
            detail="eqpt_code + ledger_code pair not found in master_table"
        )

    # -------------------------------------------------------
    # VALIDATE EQUIPMENT NAME (PRIMARY KEY)
    # -------------------------------------------------------
    existing_name = await session.scalar(
        select(cds_table).where(
            cds_table.equipment_name == payload.equipment_name
        )
    )
    if existing_name:
        raise HTTPException(
            status_code=400,
            detail="equipment_name already exists in CDS table"
        )

    # -------------------------------------------------------
    # VALIDATE GRP (UNIQUE)
    # -------------------------------------------------------
    existing_grp = await session.scalar(
        select(cds_table).where(
            cds_table.grp == payload.grp
        )
    )
    if existing_grp:
        raise HTTPException(
            status_code=400,
            detail="grp already exists — grp must remain unique"
        )

    # -------------------------------------------------------
    # INSERT NEW ROW
    # -------------------------------------------------------
    new_entry = cds_table(
        ledger_code=payload.ledger_code,
        eqpt_code=payload.eqpt_code,
        equipment_name=payload.equipment_name,
        grp=payload.grp,
        head=payload.head,
        db=payload.db,   # db is NOT UNIQUE anymore
    )

    session.add(new_entry)
    await session.commit()
    await session.refresh(new_entry)

    # -------------------------------------------------------
    # RETURN FORMATTED RESPONSE
    # -------------------------------------------------------
    return {
        "eqpt_name": new_entry.equipment_name,
        "Database": new_entry.db,
        "head": new_entry.head,
        "eqpt_code": new_entry.eqpt_code,
        "ledger_code": new_entry.ledger_code,
        "grp": new_entry.grp,
    }