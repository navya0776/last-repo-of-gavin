# routes/ledger_routes.py
from fastapi import APIRouter
from crud_ledger import ledger_service, ledger_analytics, StoreLedgerDocument, LedgerMaintenance

router = APIRouter(prefix="/ledger", tags=["Ledger"])

# ---------- BASIC CRUD ----------
@router.post("/create")
async def create_ledger(data: StoreLedgerDocument):
    return await ledger_service.create_ledger(data)

@router.get("/all")
async def get_all_ledgers():
    return await ledger_service.get_all_ledgers()

@router.get("/{equipment_code}")
async def get_ledger(equipment_code: str):
    return await ledger_service.get_ledger_by_equipment_code(equipment_code)

@router.post("/{equipment_code}/add-page")
async def add_page(equipment_code: str, page: LedgerMaintenance):
    return await ledger_service.add_ledger_page(equipment_code, page)

@router.put("/update/{ledger_page_name}")
async def update_ledger_page(ledger_page_name: str, updated_data: dict):
    return await ledger_service.update_ledger_page(ledger_page_name, updated_data)

@router.get("/search/")
async def search_ledgers(query: str):
    return await ledger_service.search_ledgers(query)

@router.get("/filter/")
async def filter_ledgers(field: str, value: str):
    return await ledger_service.filter_ledgers(field, value)

@router.get("/export/")
async def export_to_excel(report_type: str, start_date: str = None, end_date: str = None):
    return await ledger_service.export_to_excel(report_type, start_date, end_date)


# ---------- ANALYTICS ----------
@router.get("/analysis/overhaul")
async def overhaul_report(start_date: str = None, end_date: str = None):
    return await ledger_analytics.get_overhaul_report(start_date, end_date)

@router.get("/analysis/status")
async def equipment_status(equipment_code: str = None, status_type: str = None):
    return await ledger_analytics.get_equipment_status(equipment_code, status_type)

@router.get("/analysis/parts")
async def parts_analysis(equipment_code: str = None, analysis_type: str = None):
    return await ledger_analytics.get_parts_analysis(equipment_code, analysis_type)

@router.get("/analysis/stock")
async def current_stock(equipment_code: str = None):
    return await ledger_analytics.get_current_stock(equipment_code)
