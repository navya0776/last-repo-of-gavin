from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.CDS.cds import (
    AddEquipmentCreate,
    CDSView_primary,
    JobMasterCreate,
    JobMasterView,
)
from backend.utils.users import UserPermissions
from data.database import get_db
from data.models.cds import cds_table, JobMaster
from data.models.master_tbl import MasterTable

router = APIRouter()


# ============================================================
#  GET ALL ENTRIES FROM cds_table
# ============================================================
@router.get(
    "/",
    response_model=list[CDSView_primary],
    description="List's all the equipments in CDS",
)
async def list_all_equipment(
    perms: UserPermissions, session: AsyncSession = Depends(get_db)
):
    if not perms.cds.read:
        raise HTTPException(status_code=403, detail="Not allowed to read CDS")

    result = await session.scalars(select(cds_table))

    return [CDSView_primary.model_validate(row) for row in result.all()]


# ============================================================
#  ADD EQUIPMENT ENTRY INTO cds_table
# ============================================================


@router.post("/")
async def add_equipment(
    payload: AddEquipmentCreate,
    perms: UserPermissions,
    session: AsyncSession = Depends(get_db),
):
    if not perms.cds.write:
        raise HTTPException(status_code=403, detail="Not allowed to write CDS")

    # -------------------------------------------------------
    # VALIDATE THAT eqpt_code + ledger_code EXIST IN MASTER TABLE
    # (you MUST keep this because schema doesn't enforce it)
    # -------------------------------------------------------
    master_exists = await session.scalar(
        select(MasterTable).where(
            MasterTable.eqpt_code == payload.eqpt_code,
            MasterTable.Ledger_code == payload.ledger_code,
        )
    )
    if not master_exists:
        raise HTTPException(
            status_code=400,
            detail="eqpt_code + ledger_code pair not found in master_table",
        )

    # -------------------------------------------------------
    # INSERT WITH DB-LEVEL SAFETY FOR UNIQUE CONSTRAINTS
    # -------------------------------------------------------
    try:
        await session.execute(insert(cds_table).values(**payload.model_dump()))

    except IntegrityError as e:
        await session.rollback()
        msg = str(e.orig)

        if "equipment_name" in msg:
            raise HTTPException(400, "equipment_name already exists")

        if "grp" in msg:
            raise HTTPException(400, "grp must be unique")

        raise HTTPException(500, "Database error")


@router.get("/job-master/{equipment_code}", response_model=list[JobMasterView])
async def get_jobs(
    equipment_code: str,
    permissions: UserPermissions,
    session: AsyncSession = Depends(get_db),
):
    if not permissions.cds.read:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient permissions!"
        )

    result = await session.scalars(
        select(JobMaster).where(JobMaster.eqpt_code == equipment_code)
    )

    return result.all()


@router.post("/job-master")
async def create_job(
    payload: JobMasterCreate,
    permissions: UserPermissions,
    session: AsyncSession = Depends(get_db),
):
    if not permissions.cds.write:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient permissions!"
        )

    try:
        await session.execute(insert(JobMaster))

    except IntegrityError as e:
        await session.rollback()
