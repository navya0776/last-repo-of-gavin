import asyncio

from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas.ledger import (
    LedgerMaintanenceCreate,
    LedgerMaintanenceUpdate,
    LedgerMaintenanceResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.ledger.stk_analysis import StockAnalysisResult
from backend.schemas.ledger.ledgers import StoreResponse

from backend.services.ledger import (
    add_page,
    get_all_ledgers,
    get_could_change_analysis,
    get_desirable_analysis,
    get_essential_analysis,
    get_item_analysis,
    get_ledger_pages,
    get_msc_analysis,
    get_must_change_analysis,
    get_non_scaled_item_analysis,
    get_scaled_item_analysis,
    get_shoud_change_analysis,
    get_ved_analysis,
    get_vital_analysis,
    update_page,
)
from backend.utils.users import UserPermissions
from data.database import get_db

router = APIRouter()


@router.get("/", response_model=list[StoreResponse])
async def get_all_ledger(
    permissions: UserPermissions, session: AsyncSession = Depends(get_db)
):
    if permissions.ledger.read:
        return await get_all_ledgers(session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Read permissions not found!"
    )


@router.get("/{ledger_code}", response_model=list[LedgerMaintenanceResponse])
async def get_ledger_page(
    permissions: UserPermissions,
    ledger_code: str,
    session: AsyncSession = Depends(get_db),
):
    if not ledger_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Provide either ledger_name or ledger_code!",
        )

    if permissions.ledger.read:
        return await get_ledger_pages(ledger_code, session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Read permissions not found!"
    )


@router.post("/")
async def add_ledger_page(
    permissions: UserPermissions,
    ledger_page: LedgerMaintanenceCreate,
    ledger_code: str = Query(...),
    session: AsyncSession = Depends(get_db),
):
    if not permissions.ledger.read:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Read permissions not found!",
        )
    if permissions.ledger.write:
        return await add_page(ledger_code, ledger_page, session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No write permissions",
    )


@router.put("/")
async def update_ledger_page(
    permissions: UserPermissions,
    ledger_page: LedgerMaintanenceUpdate,
    ledger_code: str = Query(...),
    session: AsyncSession = Depends(get_db),
):
    if not permissions.ledger.read:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Read permissions not found!",
        )

    if permissions.ledger.write:
        return await update_page(ledger_code, ledger_page, session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No write permissions",
    )


@router.post("/analysis", response_model=StockAnalysisResult)
async def ledger_analysis(
    permissions: UserPermissions,
    ledger_code: str = Query(...),
    session: AsyncSession = Depends(get_db),
):
    if not permissions.ledger.read:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No read permissions"
        )
    (
        no_of_items,
        scaled_items,
        non_scaled_items,
        msc,
        must_change,
        should_change,
        could_change,
        ved,
        vital,
        essential,
        desirable,
    ) = await asyncio.gather(
        get_item_analysis(ledger_code, session),
        get_scaled_item_analysis(ledger_code, session),
        get_non_scaled_item_analysis(ledger_code, session),
        get_msc_analysis(ledger_code, session),
        get_must_change_analysis(ledger_code, session),
        get_shoud_change_analysis(ledger_code, session),
        get_could_change_analysis(ledger_code, session),
        get_ved_analysis(ledger_code, session),
        get_vital_analysis(ledger_code, session),
        get_essential_analysis(ledger_code, session),
        get_desirable_analysis(ledger_code, session),
    )

    return StockAnalysisResult(
        no_of_items=no_of_items,
        scl_itms=scaled_items,
        nsc_itms=non_scaled_items,
        ved=ved,
        vital=vital,
        essential=essential,
        desirable=desirable,
        msc=msc,
        mst_chng=must_change,
        cld_chng=could_change,
        shld_chng=should_change,
    )
