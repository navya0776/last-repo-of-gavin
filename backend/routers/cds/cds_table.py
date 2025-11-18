from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.schemas.CDS.cds import AddEquipmentCreate, AddEquipmentView,CDSView_primary
from backend.utils.users import UserPermissions
from data.database import get_db
from data.models.cds import cds_table

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

    # Check duplicate entry using composite key
    existing = await session.scalar(
        select(cds_table).where(
            cds_table.eqpt_code == payload.eqpt_code,
            cds_table.ledger_code == payload.ledger_code
        )
    )
    if existing:
        raise HTTPException(status_code=400, detail="Equipment already exists in CDS table")

    # Insert new row
    new_entry = cds_table(
        ledger_code=payload.ledger_code,
        eqpt_code=payload.eqpt_code,
        equipment_name=payload.equipment_name,
        grp=payload.grp,
        head=payload.head,
        db=payload.db,
    )

    session.add(new_entry)
    await session.commit()
    await session.refresh(new_entry)

    # Return CDSView_primary mapping
    return {
        "eqpt_name": new_entry.equipment_name,
        "Database": new_entry.db,
        "head": new_entry.head,
        "eqpt_code": new_entry.eqpt_code,
        "ledger_code": new_entry.ledger_code,
        "grp": new_entry.grp,
    }