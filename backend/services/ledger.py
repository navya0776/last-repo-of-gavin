from logging import getLogger

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from backend.schemas.ledger import (
    LedgerMaintanenceCreate,
    LedgerMaintanenceUpdate,
    LedgerMaintenanceResponse,
)
from backend.schemas.ledger.stk_analysis import StockCategoryBreakdown
from data.database import DBSession
from data.models.ledgers import MSC, VED, AllStores, Ledger, LedgerMaintenance

logger = getLogger(__name__)


async def get_all_ledgers(session=DBSession):
    result = await session.execute(
        select(AllStores).options(selectinload(AllStores.ledgers))
    )

    return result.scalars().all()


async def get_ledger_pages(
    ledger_name: str | None = None,
    ledger_code: str | None = None,
    session=DBSession,
) -> list[LedgerMaintenanceResponse]:
    # Find the ledger code if only name is given
    if not ledger_code:
        result = await session.execute(
            select(Ledger.Ledger_code).where(Ledger.Ledger_name == ledger_name)
        )
        ledger_code = result.scalar_one_or_none()
        if not ledger_code:
            raise HTTPException(status_code=404, detail="Ledger not found")

    # Now query maintenance records directly (lazy, efficient)
    stmt = select(LedgerMaintenance).where(LedgerMaintenance.ledger_code == ledger_code)
    result = await session.stream_scalars(stmt)
    # stream_scalars → yields results as they come, not all in memory

    pages = []
    async for record in result:
        pages.append(
            LedgerMaintenanceResponse.model_validate(record, from_attributes=True)
        )

    return pages


async def add_page(
    ledger_code: str, ledger_page: LedgerMaintanenceCreate, session=DBSession
):
    async with session.begin():
        try:
            ledger = await session.get(Ledger, ledger_code)

            if not ledger:
                logger.critical(
                    "Ledger not found but ledger page creating update was valid"
                )
                raise HTTPException(status_code=500, detail="Internal server error")

            page = LedgerMaintenance(
                **ledger_page.model_dump(), ledger_code=ledger_code
            )
            session.add(page)

            await session.flush()

        except Exception as e:
            logger.exception("Error in adding a ledger page: %s" % e)
            await session.rollback()


async def update_page(
    ledger_code: str, ledger_page: LedgerMaintanenceUpdate, session=DBSession
):
    async with session.begin():
        try:
            stmt = (
                select(LedgerMaintenance)
                .where(
                    LedgerMaintenance.ledger_code == ledger_code,
                    LedgerMaintenance.ledger_page == ledger_page.ledger_page,
                )
                .with_for_update()  # optional row lock to prevent concurrent updates
            )
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()

            if not record:
                raise HTTPException(status_code=404, detail="Page not found")

            # Apply updates (validated from Pydantic model)
            for key, value in ledger_page.model_dump(exclude_unset=True).items():
                setattr(record, key, value)

            # Transaction auto-commits on exit from `session.begin()`
            await session.flush()
            return status.HTTP_200_OK
        except:
            await session.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_msc_analysis(ledger_code: str, session=DBSession):
    """Compute stock breakdowns asynchronously."""
    # Example: group by M/S/C category
    msc_query = (
        select(
            LedgerMaintenance.msc,
            func.count().label("total_qty"),
            func.sum(LedgerMaintenance.unsv_stock).label("unsv_stk"),
            func.sum(LedgerMaintenance.rep_stock).label("rep_stk"),
            func.sum(LedgerMaintenance.serv_stock).label("ser_stk"),
            func.sum(LedgerMaintenance.dues_in).label("D_in"),
            func.sum(LedgerMaintenance.Re_ord_lvl).label("re_ord_lvl"),
            func.sum(LedgerMaintenance.safety_stk).label("safety_stk"),
            func.count(LedgerMaintenance.serv_stock == 0).label("zero_stk"),
            func.count(LedgerMaintenance.serv_stock < 2).label("stk_less_than_2"),
            func.count(LedgerMaintenance.serv_stock < 5).label("stk_less_than_5"),
            func.count(LedgerMaintenance.serv_stock < 10).label("stk_less_than_10"),
        )
        .group_by(LedgerMaintenance.msc)
        .where(LedgerMaintenance.ledger_code == ledger_code)
    )
    result = await session.execute(msc_query)
    row = result.mappings().first()

    assert row is not None, "MSC analysis returned none even though ledger was found"

    # Convert ORM results → Pydantic models
    return StockCategoryBreakdown(
        total_qty=row["total_qty"] or 0,
        unsv_stk=row["unsv_stk"] or 0,
        rep_stk=row["rep_stk"] or 0,
        ser_stk=row["ser_stk"] or 0,
        per_stk=(
            row["ser_stk"] / row["tot_stk"] * 100
        ),  # You can compute percentage here later
        D_in=row["D_in"] or 0,
        tot_stk=row["ser_stk"]
        or 0,  # Yes i know i wrote set_stk, this is litterally what it is
        per_tot_stk=0,
        re_ord_lvl=row["re_ord_lvl"] or 0,
        safety_stk=row["safety_stk"] or 0,
        zero_stk=row["zero_stk"] or 0,
        stk_less_than_2=row["stk_less_than_2"] or 0,
        stk_less_than_5=row["stk_less_than_5"] or 0,
        stk_less_than_10=row["stk_less_than_10"] or 0,
    )


async def get_ved_analysis(ledger_code: str, session=DBSession):
    """Compute stock breakdowns asynchronously."""
    # Example: group by M/S/C category
    msc_query = (
        select(
            LedgerMaintenance.ved,
            func.count().label("total_qty"),
            func.sum(LedgerMaintenance.unsv_stock).label("unsv_stk"),
            func.sum(LedgerMaintenance.rep_stock).label("rep_stk"),
            func.sum(LedgerMaintenance.serv_stock).label("ser_stk"),
            func.sum(LedgerMaintenance.dues_in).label("D_in"),
            func.sum(LedgerMaintenance.Re_ord_lvl).label("re_ord_lvl"),
            func.sum(LedgerMaintenance.safety_stk).label("safety_stk"),
            func.count(LedgerMaintenance.serv_stock == 0).label("zero_stk"),
            func.count(LedgerMaintenance.serv_stock < 2).label("stk_less_than_2"),
            func.count(LedgerMaintenance.serv_stock < 5).label("stk_less_than_5"),
            func.count(LedgerMaintenance.serv_stock < 10).label("stk_less_than_10"),
        )
        .group_by(LedgerMaintenance.ved)
        .where(LedgerMaintenance.ledger_code == ledger_code)
    )
    result = await session.execute(msc_query)
    row = result.mappings().first()

    assert row is not None, "VED analysis returned none even though ledger was found"

    # Convert ORM results → Pydantic models
    return StockCategoryBreakdown(
        total_qty=row["total_qty"] or 0,
        unsv_stk=row["unsv_stk"] or 0,
        rep_stk=row["rep_stk"] or 0,
        ser_stk=row["ser_stk"] or 0,
        per_stk=(
            row["ser_stk"] / row["tot_stk"] * 100
        ),  # You can compute percentage here later
        D_in=row["D_in"] or 0,
        tot_stk=row["ser_stk"]
        or 0,  # Yes i know i wrote set_stk, this is litterally what it is
        per_tot_stk=0,
        re_ord_lvl=row["re_ord_lvl"] or 0,
        safety_stk=row["safety_stk"] or 0,
        zero_stk=row["zero_stk"] or 0,
        stk_less_than_2=row["stk_less_than_2"] or 0,
        stk_less_than_5=row["stk_less_than_5"] or 0,
        stk_less_than_10=row["stk_less_than_10"] or 0,
    )


async def get_must_change_analysis(ledger_code: str, session=DBSession):
    """Compute stock breakdowns asynchronously."""
    # Example: group by M/S/C category
    msc_query = (
        select(
            LedgerMaintenance.msc,
            func.count().label("total_qty"),
            func.sum(LedgerMaintenance.unsv_stock).label("unsv_stk"),
            func.sum(LedgerMaintenance.rep_stock).label("rep_stk"),
            func.sum(LedgerMaintenance.serv_stock).label("ser_stk"),
            func.sum(LedgerMaintenance.dues_in).label("D_in"),
            func.sum(LedgerMaintenance.Re_ord_lvl).label("re_ord_lvl"),
            func.sum(LedgerMaintenance.safety_stk).label("safety_stk"),
            func.count(LedgerMaintenance.serv_stock == 0).label("zero_stk"),
            func.count(LedgerMaintenance.serv_stock < 2).label("stk_less_than_2"),
            func.count(LedgerMaintenance.serv_stock < 5).label("stk_less_than_5"),
            func.count(LedgerMaintenance.serv_stock < 10).label("stk_less_than_10"),
        )
        .group_by(LedgerMaintenance.msc)
        .where(LedgerMaintenance.ledger_code == ledger_code)
        .where(LedgerMaintenance.msc == MSC.M)
    )
    result = await session.execute(msc_query)
    row = result.mappings().first()

    assert row is not None, "VED analysis returned none even though ledger was found"

    # Convert ORM results → Pydantic models
    return StockCategoryBreakdown(
        total_qty=row["total_qty"] or 0,
        unsv_stk=row["unsv_stk"] or 0,
        rep_stk=row["rep_stk"] or 0,
        ser_stk=row["ser_stk"] or 0,
        per_stk=(
            row["ser_stk"] / row["tot_stk"] * 100
        ),  # You can compute percentage here later
        D_in=row["D_in"] or 0,
        tot_stk=row["ser_stk"]
        or 0,  # Yes i know i wrote set_stk, this is litterally what it is
        per_tot_stk=0,
        re_ord_lvl=row["re_ord_lvl"] or 0,
        safety_stk=row["safety_stk"] or 0,
        zero_stk=row["zero_stk"] or 0,
        stk_less_than_2=row["stk_less_than_2"] or 0,
        stk_less_than_5=row["stk_less_than_5"] or 0,
        stk_less_than_10=row["stk_less_than_10"] or 0,
    )


async def get_shoud_change_analysis(ledger_code: str, session=DBSession):
    """Compute stock breakdowns asynchronously."""
    # Example: group by M/S/C category
    msc_query = (
        select(
            LedgerMaintenance.msc,
            func.count().label("total_qty"),
            func.sum(LedgerMaintenance.unsv_stock).label("unsv_stk"),
            func.sum(LedgerMaintenance.rep_stock).label("rep_stk"),
            func.sum(LedgerMaintenance.serv_stock).label("ser_stk"),
            func.sum(LedgerMaintenance.dues_in).label("D_in"),
            func.sum(LedgerMaintenance.Re_ord_lvl).label("re_ord_lvl"),
            func.sum(LedgerMaintenance.safety_stk).label("safety_stk"),
            func.count(LedgerMaintenance.serv_stock == 0).label("zero_stk"),
            func.count(LedgerMaintenance.serv_stock < 2).label("stk_less_than_2"),
            func.count(LedgerMaintenance.serv_stock < 5).label("stk_less_than_5"),
            func.count(LedgerMaintenance.serv_stock < 10).label("stk_less_than_10"),
        )
        .group_by(LedgerMaintenance.msc)
        .where(LedgerMaintenance.ledger_code == ledger_code)
        .where(LedgerMaintenance.msc == MSC.S)
    )
    result = await session.execute(msc_query)
    row = result.mappings().first()

    assert row is not None, "VED analysis returned none even though ledger was found"

    # Convert ORM results → Pydantic models
    return StockCategoryBreakdown(
        total_qty=row["total_qty"] or 0,
        unsv_stk=row["unsv_stk"] or 0,
        rep_stk=row["rep_stk"] or 0,
        ser_stk=row["ser_stk"] or 0,
        per_stk=(
            row["ser_stk"] / row["tot_stk"] * 100
        ),  # You can compute percentage here later
        D_in=row["D_in"] or 0,
        tot_stk=row["ser_stk"]
        or 0,  # Yes i know i wrote set_stk, this is litterally what it is
        per_tot_stk=0,
        re_ord_lvl=row["re_ord_lvl"] or 0,
        safety_stk=row["safety_stk"] or 0,
        zero_stk=row["zero_stk"] or 0,
        stk_less_than_2=row["stk_less_than_2"] or 0,
        stk_less_than_5=row["stk_less_than_5"] or 0,
        stk_less_than_10=row["stk_less_than_10"] or 0,
    )


async def get_could_change_analysis(ledger_code: str, session=DBSession):
    """Compute stock breakdowns asynchronously."""
    # Example: group by M/S/C category
    msc_query = (
        select(
            LedgerMaintenance.msc,
            func.count().label("total_qty"),
            func.sum(LedgerMaintenance.unsv_stock).label("unsv_stk"),
            func.sum(LedgerMaintenance.rep_stock).label("rep_stk"),
            func.sum(LedgerMaintenance.serv_stock).label("ser_stk"),
            func.sum(LedgerMaintenance.dues_in).label("D_in"),
            func.sum(LedgerMaintenance.Re_ord_lvl).label("re_ord_lvl"),
            func.sum(LedgerMaintenance.safety_stk).label("safety_stk"),
            func.count(LedgerMaintenance.serv_stock == 0).label("zero_stk"),
            func.count(LedgerMaintenance.serv_stock < 2).label("stk_less_than_2"),
            func.count(LedgerMaintenance.serv_stock < 5).label("stk_less_than_5"),
            func.count(LedgerMaintenance.serv_stock < 10).label("stk_less_than_10"),
        )
        .group_by(LedgerMaintenance.msc)
        .where(LedgerMaintenance.ledger_code == ledger_code)
        .where(LedgerMaintenance.msc == MSC.C)
    )
    result = await session.execute(msc_query)
    row = result.mappings().first()

    assert row is not None, "VED analysis returned none even though ledger was found"

    # Convert ORM results → Pydantic models
    return StockCategoryBreakdown(
        total_qty=row["total_qty"] or 0,
        unsv_stk=row["unsv_stk"] or 0,
        rep_stk=row["rep_stk"] or 0,
        ser_stk=row["ser_stk"] or 0,
        per_stk=(
            row["ser_stk"] / row["tot_stk"] * 100
        ),  # You can compute percentage here later
        D_in=row["D_in"] or 0,
        tot_stk=row["ser_stk"]
        or 0,  # Yes i know i wrote set_stk, this is litterally what it is
        per_tot_stk=0,
        re_ord_lvl=row["re_ord_lvl"] or 0,
        safety_stk=row["safety_stk"] or 0,
        zero_stk=row["zero_stk"] or 0,
        stk_less_than_2=row["stk_less_than_2"] or 0,
        stk_less_than_5=row["stk_less_than_5"] or 0,
        stk_less_than_10=row["stk_less_than_10"] or 0,
    )


async def get_vital_analysis(ledger_code: str, session=DBSession):
    """Compute stock breakdowns asynchronously."""
    # Example: group by M/S/C category
    msc_query = (
        select(
            LedgerMaintenance.ved,
            func.count().label("total_qty"),
            func.sum(LedgerMaintenance.unsv_stock).label("unsv_stk"),
            func.sum(LedgerMaintenance.rep_stock).label("rep_stk"),
            func.sum(LedgerMaintenance.serv_stock).label("ser_stk"),
            func.sum(LedgerMaintenance.dues_in).label("D_in"),
            func.sum(LedgerMaintenance.Re_ord_lvl).label("re_ord_lvl"),
            func.sum(LedgerMaintenance.safety_stk).label("safety_stk"),
            func.count(LedgerMaintenance.serv_stock == 0).label("zero_stk"),
            func.count(LedgerMaintenance.serv_stock < 2).label("stk_less_than_2"),
            func.count(LedgerMaintenance.serv_stock < 5).label("stk_less_than_5"),
            func.count(LedgerMaintenance.serv_stock < 10).label("stk_less_than_10"),
        )
        .group_by(LedgerMaintenance.ved)
        .where(LedgerMaintenance.ledger_code == ledger_code)
        .where(LedgerMaintenance.ved == VED.V)
    )
    result = await session.execute(msc_query)
    row = result.mappings().first()

    assert row is not None, "VED analysis returned none even though ledger was found"

    # Convert ORM results → Pydantic models
    return StockCategoryBreakdown(
        total_qty=row["total_qty"] or 0,
        unsv_stk=row["unsv_stk"] or 0,
        rep_stk=row["rep_stk"] or 0,
        ser_stk=row["ser_stk"] or 0,
        per_stk=(
            row["ser_stk"] / row["tot_stk"] * 100
        ),  # You can compute percentage here later
        D_in=row["D_in"] or 0,
        tot_stk=row["ser_stk"]
        or 0,  # Yes i know i wrote set_stk, this is litterally what it is
        per_tot_stk=0,
        re_ord_lvl=row["re_ord_lvl"] or 0,
        safety_stk=row["safety_stk"] or 0,
        zero_stk=row["zero_stk"] or 0,
        stk_less_than_2=row["stk_less_than_2"] or 0,
        stk_less_than_5=row["stk_less_than_5"] or 0,
        stk_less_than_10=row["stk_less_than_10"] or 0,
    )


async def get_essential_analysis(ledger_code: str, session=DBSession):
    """Compute stock breakdowns asynchronously."""
    # Example: group by M/S/C category
    msc_query = (
        select(
            LedgerMaintenance.ved,
            func.count().label("total_qty"),
            func.sum(LedgerMaintenance.unsv_stock).label("unsv_stk"),
            func.sum(LedgerMaintenance.rep_stock).label("rep_stk"),
            func.sum(LedgerMaintenance.serv_stock).label("ser_stk"),
            func.sum(LedgerMaintenance.dues_in).label("D_in"),
            func.sum(LedgerMaintenance.Re_ord_lvl).label("re_ord_lvl"),
            func.sum(LedgerMaintenance.safety_stk).label("safety_stk"),
            func.count(LedgerMaintenance.serv_stock == 0).label("zero_stk"),
            func.count(LedgerMaintenance.serv_stock < 2).label("stk_less_than_2"),
            func.count(LedgerMaintenance.serv_stock < 5).label("stk_less_than_5"),
            func.count(LedgerMaintenance.serv_stock < 10).label("stk_less_than_10"),
        )
        .group_by(LedgerMaintenance.ved)
        .where(LedgerMaintenance.ledger_code == ledger_code)
        .where(LedgerMaintenance.ved == VED.E)
    )
    result = await session.execute(msc_query)
    row = result.mappings().first()

    assert row is not None, "VED analysis returned none even though ledger was found"

    # Convert ORM results → Pydantic models
    return StockCategoryBreakdown(
        total_qty=row["total_qty"] or 0,
        unsv_stk=row["unsv_stk"] or 0,
        rep_stk=row["rep_stk"] or 0,
        ser_stk=row["ser_stk"] or 0,
        per_stk=(
            row["ser_stk"] / row["tot_stk"] * 100
        ),  # You can compute percentage here later
        D_in=row["D_in"] or 0,
        tot_stk=row["ser_stk"]
        or 0,  # Yes i know i wrote set_stk, this is litterally what it is
        per_tot_stk=0,
        re_ord_lvl=row["re_ord_lvl"] or 0,
        safety_stk=row["safety_stk"] or 0,
        zero_stk=row["zero_stk"] or 0,
        stk_less_than_2=row["stk_less_than_2"] or 0,
        stk_less_than_5=row["stk_less_than_5"] or 0,
        stk_less_than_10=row["stk_less_than_10"] or 0,
    )


async def get_desirable_analysis(ledger_code: str, session=DBSession):
    """Compute stock breakdowns asynchronously."""
    # Example: group by M/S/C category
    msc_query = (
        select(
            LedgerMaintenance.ved,
            func.count().label("total_qty"),
            func.sum(LedgerMaintenance.unsv_stock).label("unsv_stk"),
            func.sum(LedgerMaintenance.rep_stock).label("rep_stk"),
            func.sum(LedgerMaintenance.serv_stock).label("ser_stk"),
            func.sum(LedgerMaintenance.dues_in).label("D_in"),
            func.sum(LedgerMaintenance.Re_ord_lvl).label("re_ord_lvl"),
            func.sum(LedgerMaintenance.safety_stk).label("safety_stk"),
            func.count(LedgerMaintenance.serv_stock == 0).label("zero_stk"),
            func.count(LedgerMaintenance.serv_stock < 2).label("stk_less_than_2"),
            func.count(LedgerMaintenance.serv_stock < 5).label("stk_less_than_5"),
            func.count(LedgerMaintenance.serv_stock < 10).label("stk_less_than_10"),
        )
        .group_by(LedgerMaintenance.ved)
        .where(LedgerMaintenance.ledger_code == ledger_code)
        .where(LedgerMaintenance.ved == VED.D)
    )
    result = await session.execute(msc_query)
    row = result.mappings().first()

    assert row is not None, "VED analysis returned none even though ledger was found"

    # Convert ORM results → Pydantic models
    return StockCategoryBreakdown(
        total_qty=row["total_qty"] or 0,
        unsv_stk=row["unsv_stk"] or 0,
        rep_stk=row["rep_stk"] or 0,
        ser_stk=row["ser_stk"] or 0,
        per_stk=(
            row["ser_stk"] / row["tot_stk"] * 100
        ),  # You can compute percentage here later
        D_in=row["D_in"] or 0,
        tot_stk=row["ser_stk"]
        or 0,  # Yes i know i wrote set_stk, this is litterally what it is
        per_tot_stk=0,
        re_ord_lvl=row["re_ord_lvl"] or 0,
        safety_stk=row["safety_stk"] or 0,
        zero_stk=row["zero_stk"] or 0,
        stk_less_than_2=row["stk_less_than_2"] or 0,
        stk_less_than_5=row["stk_less_than_5"] or 0,
        stk_less_than_10=row["stk_less_than_10"] or 0,
    )


async def get_item_analysis(ledger_code: str, session=DBSession):
    """Compute stock breakdowns asynchronously."""
    # Example: group by M/S/C category
    msc_query = select(
        LedgerMaintenance,
        func.count().label("total_qty"),
        func.sum(LedgerMaintenance.unsv_stock).label("unsv_stk"),
        func.sum(LedgerMaintenance.rep_stock).label("rep_stk"),
        func.sum(LedgerMaintenance.serv_stock).label("ser_stk"),
        func.sum(LedgerMaintenance.dues_in).label("D_in"),
        func.sum(LedgerMaintenance.Re_ord_lvl).label("re_ord_lvl"),
        func.sum(LedgerMaintenance.safety_stk).label("safety_stk"),
        func.count(LedgerMaintenance.serv_stock == 0).fi.label("zero_stk"),
        func.count(LedgerMaintenance.serv_stock < 2).label("stk_less_than_2"),
        func.count(LedgerMaintenance.serv_stock < 5).label("stk_less_than_5"),
        func.count(LedgerMaintenance.serv_stock < 10).label("stk_less_than_10"),
    ).where(LedgerMaintenance.ledger_code == ledger_code)
    result = await session.execute(msc_query)
    row = result.mappings().first()

    assert row is not None, "VED analysis returned none even though ledger was found"

    # Convert ORM results → Pydantic models
    return StockCategoryBreakdown(
        total_qty=row["total_qty"] or 0,
        unsv_stk=row["unsv_stk"] or 0,
        rep_stk=row["rep_stk"] or 0,
        ser_stk=row["ser_stk"] or 0,
        per_stk=(
            row["ser_stk"] / row["tot_stk"] * 100
        ),  # You can compute percentage here later
        D_in=row["D_in"] or 0,
        tot_stk=row["ser_stk"]
        or 0,  # Yes i know i wrote set_stk, this is litterally what it is
        per_tot_stk=0,
        re_ord_lvl=row["re_ord_lvl"] or 0,
        safety_stk=row["safety_stk"] or 0,
        zero_stk=row["zero_stk"] or 0,
        stk_less_than_2=row["stk_less_than_2"] or 0,
        stk_less_than_5=row["stk_less_than_5"] or 0,
        stk_less_than_10=row["stk_less_than_10"] or 0,
    )


async def get_scaled_item_analysis(ledger_code: str, session=DBSession):
    """Compute stock breakdowns asynchronously."""
    # Example: group by M/S/C category
    msc_query = (
        select(
            LedgerMaintenance.ohs_number,
            func.count().label("total_qty"),
            func.sum(LedgerMaintenance.unsv_stock).label("unsv_stk"),
            func.sum(LedgerMaintenance.rep_stock).label("rep_stk"),
            func.sum(LedgerMaintenance.serv_stock).label("ser_stk"),
            func.sum(LedgerMaintenance.dues_in).label("D_in"),
            func.sum(LedgerMaintenance.Re_ord_lvl).label("re_ord_lvl"),
            func.sum(LedgerMaintenance.safety_stk).label("safety_stk"),
            func.count(LedgerMaintenance.serv_stock == 0).label("zero_stk"),
            func.count(LedgerMaintenance.serv_stock < 2).label("stk_less_than_2"),
            func.count(LedgerMaintenance.serv_stock < 5).label("stk_less_than_5"),
            func.count(LedgerMaintenance.serv_stock < 10).label("stk_less_than_10"),
        )
        .group_by(LedgerMaintenance.ohs_number)
        .where(LedgerMaintenance.ledger_code == ledger_code)
        .where(LedgerMaintenance.ohs_number != "NS")
    )
    result = await session.execute(msc_query)
    row = result.mappings().first()

    assert row is not None, "VED analysis returned none even though ledger was found"

    # Convert ORM results → Pydantic models
    return StockCategoryBreakdown(
        total_qty=row["total_qty"] or 0,
        unsv_stk=row["unsv_stk"] or 0,
        rep_stk=row["rep_stk"] or 0,
        ser_stk=row["ser_stk"] or 0,
        per_stk=(
            row["ser_stk"] / row["tot_stk"] * 100
        ),  # You can compute percentage here later
        D_in=row["D_in"] or 0,
        tot_stk=row["ser_stk"]
        or 0,  # Yes i know i wrote set_stk, this is litterally what it is
        per_tot_stk=0,
        re_ord_lvl=row["re_ord_lvl"] or 0,
        safety_stk=row["safety_stk"] or 0,
        zero_stk=row["zero_stk"] or 0,
        stk_less_than_2=row["stk_less_than_2"] or 0,
        stk_less_than_5=row["stk_less_than_5"] or 0,
        stk_less_than_10=row["stk_less_than_10"] or 0,
    )


async def get_non_scaled_item_analysis(ledger_code: str, session=DBSession):
    """Compute stock breakdowns asynchronously."""
    # Example: group by M/S/C category
    msc_query = (
        select(
            LedgerMaintenance.ohs_number,
            func.count().label("total_qty"),
            func.sum(LedgerMaintenance.unsv_stock).label("unsv_stk"),
            func.sum(LedgerMaintenance.rep_stock).label("rep_stk"),
            func.sum(LedgerMaintenance.serv_stock).label("ser_stk"),
            func.sum(LedgerMaintenance.dues_in).label("D_in"),
            func.sum(LedgerMaintenance.Re_ord_lvl).label("re_ord_lvl"),
            func.sum(LedgerMaintenance.safety_stk).label("safety_stk"),
            func.count(LedgerMaintenance.serv_stock == 0).label("zero_stk"),
            func.count(LedgerMaintenance.serv_stock < 2).label("stk_less_than_2"),
            func.count(LedgerMaintenance.serv_stock < 5).label("stk_less_than_5"),
            func.count(LedgerMaintenance.serv_stock < 10).label("stk_less_than_10"),
        )
        .group_by(LedgerMaintenance.ohs_number)
        .where(LedgerMaintenance.ledger_code == ledger_code)
        .where(LedgerMaintenance.ohs_number == "NS")
    )
    result = await session.execute(msc_query)
    row = result.mappings().first()

    assert row is not None, "VED analysis returned none even though ledger was found"

    # Convert ORM results → Pydantic models
    return StockCategoryBreakdown(
        total_qty=row["total_qty"] or 0,
        unsv_stk=row["unsv_stk"] or 0,
        rep_stk=row["rep_stk"] or 0,
        ser_stk=row["ser_stk"] or 0,
        per_stk=(
            row["ser_stk"] / row["tot_stk"] * 100
        ),  # You can compute percentage here later
        D_in=row["D_in"] or 0,
        tot_stk=row["ser_stk"]
        or 0,  # Yes i know i wrote set_stk, this is litterally what it is
        per_tot_stk=0,
        re_ord_lvl=row["re_ord_lvl"] or 0,
        safety_stk=row["safety_stk"] or 0,
        zero_stk=row["zero_stk"] or 0,
        stk_less_than_2=row["stk_less_than_2"] or 0,
        stk_less_than_5=row["stk_less_than_5"] or 0,
        stk_less_than_10=row["stk_less_than_10"] or 0,
    )
