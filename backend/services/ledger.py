from sqlalchemy import select
from sqlalchemy.orm import selectinload

from data.database import DBSession
from data.models.ledgers import AllStores


async def get_all_ledgers(session=DBSession):
    result = await session.execute(
        select(AllStores).options(selectinload(AllStores.ledgers))
    )

    return result.scalars().all()
