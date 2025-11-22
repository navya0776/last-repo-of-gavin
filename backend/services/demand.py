from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from data.models import Demand, Dmd_junction, MasterTable
from backend.schemas.demand import (
    DemandCreate,
    DemandResponse,
    DmdJunctionResponse,
    EquiptmentResponse,
)


# TODO: Change this according to the newly found "On selection" feature in APD
async def create_demand(request: DemandCreate, session: AsyncSession):
    result = await session.execute(
        select(Demand).where(Demand.eqpt_code == request.eqpt_code)
    )
    eqpt = result.scalar_one_or_none()
    if not eqpt:
        raise HTTPException(
            status_code=403, detail=f"Equipment '{request.eqpt_code}' not found"
        )

    new_demand = Demand(**request.model_dump())

    session.add(new_demand)


async def _get_demand(
    demand_no: int | None, session: AsyncSession
) -> list[DemandResponse]:
    if demand_no:
        query = (
            select(Demand)
            .where(Demand.demand_no == int(demand_no))
            .order_by(Demand.fin_year.asc())
        )

    else:
        query = select(Demand).order_by(Demand.fin_year.asc())

    result = await session.execute(query)
    demand = result.scalars().all()

    if demand is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Demand not found!"
        )

    return [DemandResponse.model_validate(dem) for dem in demand]


async def _delete_demand(demand_no: int, session: AsyncSession):
    result = await session.execute(
        select(Demand).where(Demand.demand_no == int(demand_no))
    )
    demand = result.scalar_one_or_none()
    if not demand:
        raise HTTPException(status_code=404, detail=f"Demand {demand_no} not found")

    # Prevent deleting locked demands
    if demand.is_locked:
        raise HTTPException(status_code=403, detail="Cannot delete a locked demand.")

    await session.delete(demand)


async def _lock_demand(demand_no: int, session: AsyncSession):
    result = await session.execute(
        select(Demand).where(Demand.demand_no == int(demand_no))
    )
    demand = result.scalar_one_or_none()
    if not demand:
        raise HTTPException(status_code=404, detail=f"Demand {demand_no} not found")

    if demand.is_locked:
        raise HTTPException(status_code=400, detail="Demand is already locked.")

    demand.is_locked = True


async def _unlock_demand(demand_no: int, session: AsyncSession):
    result = await session.execute(
        select(Demand).where(Demand.demand_no == int(demand_no))
    )
    demand = result.scalar_one_or_none()
    if not demand:
        raise HTTPException(status_code=404, detail=f"Demand {demand_no} not found")

    if demand.is_locked:
        raise HTTPException(status_code=400, detail="Demand is not locked.")

    demand.is_locked = True


async def _list_all_equipment(session: AsyncSession) -> list[EquiptmentResponse]:
    result = await session.execute(select(MasterTable))
    equipments = result.scalars().all()
    return [EquiptmentResponse.model_validate(eqpt) for eqpt in equipments]


async def _list_demands(
    demand_no: int, session: AsyncSession
) -> list[DmdJunctionResponse]:
    result = await session.scalars(
        select(Dmd_junction).where(Dmd_junction.demand_no == int(demand_no))
    )

    return [DmdJunctionResponse.model_validate(row) for row in result.all()]
