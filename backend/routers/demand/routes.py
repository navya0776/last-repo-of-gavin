from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from data.database import get_db

from backend.services.demand import (
    create_demand,
    _get_demand,
    _delete_demand,
    _list_demands,
    _lock_demand,
    _unlock_demand,
    _list_all_equipment,
)
from backend.utils.users import UserPermissions
from backend.schemas.demand import (
    DemandCreate,
    DemandResponse,
    DmdJunctionResponse,
    EquiptmentResponse,
)

router = APIRouter()


# ===========================================
# 🆕 CREATE DEMAND
# ===========================================
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_ap_demand(
    request: DemandCreate,
    permissions: UserPermissions,
    session: AsyncSession = Depends(get_db),
):
    if permissions.apd.write:
        await create_demand(request, session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Insufficient permissions to create demand.",
    )


# ===========================================
# 📋 GET ALL DEMANDS
# ===========================================
@router.get("/", response_model=list[DemandResponse])
async def get_all_demands(
    permissions: UserPermissions,
    session: AsyncSession = Depends(get_db),
):
    if permissions.apd.read:
        return await _get_demand(None, session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Insufficient permissions to create demand.",
    )


# ===========================================
# 🔍 GET SINGLE DEMAND
# ===========================================
@router.get("/{demand_no}", response_model=list[DemandResponse])
async def get_demand_by_no(
    demand_no: int,
    permissions: UserPermissions,
    session: AsyncSession = Depends(get_db),
):
    if permissions.apd.read:
        return await _get_demand(demand_no, session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Insufficient permissions",
    )


# ===========================================
# 🗑 DELETE DEMAND
# ===========================================
@router.delete("/{demand_no}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_demand(
    demand_no: int,
    permissions: UserPermissions,
    session: AsyncSession = Depends(get_db),
):
    if permissions.apd.write:
        await _delete_demand(demand_no, session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Insufficient permissions",
    )


# ===========================================
# 🔒 LOCK DEMAND
# ===========================================
@router.post("/{demand_no}/lock")
async def lock_demand(
    demand_no: int,
    permissions: UserPermissions,
    session: AsyncSession = Depends(get_db),
):
    if permissions.apd.write:
        await _lock_demand(demand_no, session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient permissions"
    )


# ===========================================
# 🔓 UNLOCK DEMAND
# ===========================================
@router.post("/{demand_no}/unlock")
async def unlock_demand(
    demand_no: int,
    permissions: UserPermissions,
    session: AsyncSession = Depends(get_db),
):
    if permissions.apd.write:
        await _unlock_demand(demand_no, session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient permissions"
    )


@router.get("/detail/{demand_no}", response_model=list[DmdJunctionResponse])
async def list_demand(
    demand_no: int,
    permissions: UserPermissions,
    session: AsyncSession = Depends(get_db),
):
    if permissions.apd.read:
        return await _list_demands(demand_no, session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient permissions"
    )


# ===========================================
# ⚙️ LIST EQUIPMENTS
# ===========================================
@router.get("/equipments/", response_model=list[EquiptmentResponse])
async def list_all_equipments(
    permissions: UserPermissions, session: AsyncSession = Depends(get_db)
):
    if permissions.apd.read:
        return await _list_all_equipment(session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient permissions"
    )
