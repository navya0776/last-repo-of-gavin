import asyncio

from fastapi import APIRouter, HTTPException, Query, status
from schemas.ledger import (
    LedgerMaintanenceCreate,
    LedgerMaintanenceUpdate,
    LedgerMaintenanceResponse,
)
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

router = APIRouter()


@router.get("/", response_model=list[StoreResponse])
async def get_all_ledger(permissions: UserPermissions):
    """
    Will return this format

        [
    {
        "store_id": 1,
        "store_name": "Central Store",
        "ledgers": [
        {
            "Ledger_code": "L001",
            "Ledger_name": "Cash Ledger",
            "store_id": 1
        },
        {
            "Ledger_code": "L002",
            "Ledger_name": "Sales Ledger",
            "store_id": 1
        }
        ]
    }
    ]

    """
    if permissions.ledger.read:
        return await get_all_ledgers()

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Read permissions not found!"
    )


@router.get("/", response_model=list[LedgerMaintenanceResponse])
async def get_ledger_page(
    permissions: UserPermissions,
    ledger_name: str | None = Query(...),
    ledger_code: str | None = Query(...),
):
    if ledger_name is None and ledger_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide either ledger_name or ledger_code",
        )
    
    if permissions.ledger.read:
        return await get_ledger_pages(ledger_name, ledger_code)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Read permissions not found!"
    )


@router.post("/")
async def add_ledger_page(
    permissions: UserPermissions,
    ledger_page: LedgerMaintanenceCreate,
    ledger_code: str = Query(...),
):
    if not permissions.ledger.read:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Read permissions not found!",
        )
    if permissions.ledger.write:
        return await add_page(ledger_code, ledger_page)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No write permissions",
    )


@router.put("/")
async def update_ledger_page(
    permissions: UserPermissions,
    ledger_page: LedgerMaintanenceUpdate,
    ledger_code: str = Query(...),
):
    if not permissions.ledger.read:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Read permissions not found!",
        )

    if permissions.ledger.write:
        return await update_page(ledger_code, ledger_page)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No write permissions",
    )


@router.post("/analysis", response_model=StockAnalysisResult)
async def ledger_analysis(permissions: UserPermissions, ledger_code: str = Query(...)):
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
        get_item_analysis(ledger_code),
        get_scaled_item_analysis(ledger_code),
        get_non_scaled_item_analysis(ledger_code),
        get_msc_analysis(ledger_code),
        get_must_change_analysis(ledger_code),
        get_shoud_change_analysis(ledger_code),
        get_could_change_analysis(ledger_code),
        get_ved_analysis(ledger_code),
        get_vital_analysis(ledger_code),
        get_essential_analysis(ledger_code),
        get_desirable_analysis(ledger_code),
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
