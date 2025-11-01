from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# Simulating database (Replace with MongoDB, PostgreSQL, etc.)
DATABASE = {}


# ---------- SCHEMAS ----------
class LedgerMaintenance(BaseModel):
    date: datetime
    description: str
    quantity: int
    cost: float


class StoreLedgerDocument(BaseModel):
    equipment_code: str
    equipment_name: str
    category: str
    location: str
    created_at: datetime = datetime.utcnow()
    maintenance_logs: List[LedgerMaintenance] = []


# ---------- SERVICE CLASS ----------
class LedgerService:
    def __init__(self):
        self.db = DATABASE

    async def create_ledger(self, data: StoreLedgerDocument):
        if data.equipment_code in self.db:
            return {"error": "Ledger already exists"}
        self.db[data.equipment_code] = data.dict()
        return {"message": "Ledger created successfully", "ledger": data}

    async def get_all_ledgers(self):
        return list(self.db.values())

    async def get_ledger_by_equipment_code(self, equipment_code: str):
        ledger = self.db.get(equipment_code)
        if not ledger:
            return {"error": "Ledger not found"}
        return ledger

    async def add_ledger_page(self, equipment_code: str, page: LedgerMaintenance):
        ledger = self.db.get(equipment_code)
        if not ledger:
            return {"error": "Ledger not found"}
        ledger["maintenance_logs"].append(page.dict())
        return {"message": "Page added successfully"}

    async def update_ledger_page(self, ledger_page_name: str, updated_data: dict):
        for code, ledger in self.db.items():
            for page in ledger["maintenance_logs"]:
                if page["description"] == ledger_page_name:
                    page.update(updated_data)
                    return {"message": "Ledger page updated successfully"}
        return {"error": "Ledger page not found"}

    async def search_ledgers(self, query: str):
        result = [
            ledger
            for ledger in self.db.values()
            if query.lower() in ledger["equipment_name"].lower()
        ]
        return result

    async def filter_ledgers(self, field: str, value: str):
        result = [
            ledger
            for ledger in self.db.values()
            if ledger.get(field) and str(ledger[field]).lower() == value.lower()
        ]
        return result

    async def export_to_excel(
        self,
        report_type: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        # In real version, generate Excel using pandas/xlsxwriter
        return {
            "message": f"Exported {report_type} report from {start_date} to {end_date}"
        }


# ---------- ANALYTICS ----------
class LedgerAnalytics:
    async def get_overhaul_report(self, start_date=None, end_date=None):
        return {"type": "overhaul_report", "data": "Overhaul data generated"}

    async def get_equipment_status(self, equipment_code=None, status_type=None):
        return {"type": "status", "data": f"Status for {equipment_code}"}

    async def get_parts_analysis(self, equipment_code=None, analysis_type=None):
        return {
            "type": "parts_analysis",
            "data": f"Parts analysis for {equipment_code}",
        }

    async def get_current_stock(self, equipment_code=None):
        return {"type": "stock_report", "data": f"Current stock for {equipment_code}"}


# ---------- SERVICE INSTANCES ----------
ledger_service = LedgerService()
ledger_analytics = LedgerAnalytics()
