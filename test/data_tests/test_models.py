import pytest
import sys
import os
from datetime import datetime
from data.models.logs import (
    AuditLog,
    LedgerAuditLog,
    DemandAuditLog,
    StockMovementLog,
    PartAuditLog,
    ChangeDetail,
    ActionType,
    ResourceType,
)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)
from data.models.legdersAndos import AllStores, AllEquipments, AllParts
from data.models.provisioning import Demand, Details

@pytest.mark.asyncio
async def test_redis_set_get(redis_client):
    await redis_client.set("test_key", "value")
    val = await redis_client.get("test_key")
    assert val == "value"


def test_allstores_schema_valid():
    schema = AllStores.model_json_schema()
    assert "properties" in schema
    assert "store_id" in schema["properties"]

def test_allstores_instantiation():
    store = AllStores(store_id="S001", location="Patiala", authority="Admin")
    assert store.store_id == "S001"

def test_allequipments_instantiation():
    eq = AllEquipments(equipment="Compressor", equipment_code="EQ01", store_id="S001")
    assert eq.equipment_code == "EQ01"

def test_allparts_schema_valid():
    schema = AllParts.model_json_schema()
    assert "properties" in schema

def test_demand_schema_valid():
    schema = Demand.model_json_schema()
    assert "properties" in schema
    assert "details" in schema["properties"]

def test_details_optional_fields():
    details = Details(
        sub_demand_number=1,
        ledger_page_number="12A",
        part_number=101,
        nomenclature="Bolt",
        A_U="Nos",
        auth=5,
        current_stock_balance=10,
        dues_in=0,
        outstanding_requested=0,
        stock_n_yr=0,
        requested_as_ohs=0,
        consumption_pattern="2/unit",
        requested_as_per_consumption=0,
        quantity_demanded=5,
        recieved=0,
        depot_control="DC1",
        depot_control_dt="2025-01-01",
        d_e_l="L"
    )
    assert details.part_number == 101
   

# -----------------Pytest for logs.py -----------------

def test_auditlog_schema_valid():
    """Ensure AuditLog schema generates correctly."""
    schema = AuditLog.model_json_schema()
    assert "properties" in schema
    assert "activity_id" in schema["properties"]
    assert "user_id" in schema["properties"]

def test_auditlog_instantiation():
    """Test creating a simple AuditLog instance."""
    log = AuditLog(
        activity_id="A001",
        user_id="U001",
        action=ActionType.STORE_CREATED,
        resource_type=ResourceType.STORE,
        resource_id="S001"
    )
    assert log.activity_id == "A001"
    assert log.action == ActionType.STORE_CREATED
    assert log.status == "success"
    assert isinstance(log.timestamp, datetime)


# ----------------- Ledger Audit Log -----------------

def test_ledger_audit_log_instantiation():
    """Test creating a LedgerAuditLog entry."""
    log = LedgerAuditLog(
        activity_id="L001",
        user_id="U001",
        action="ledger_created",
        ledger_page="12A",
        part_number=101,
        nomenclature="Bolt",
        store_id="S001",
        changes=[
            ChangeDetail(field_name="stock", old_value=10, new_value=15)
        ],
        details={"remarks": "Initial entry"}
    )
    assert log.action == "ledger_created"
    assert log.ledger_page == "12A"
    assert log.details["remarks"] == "Initial entry"
    assert isinstance(log.timestamp, datetime)


# ----------------- Demand Audit Log -----------------

def test_demand_audit_log_instantiation():
    """Test DemandAuditLog with optional fields."""
    log = DemandAuditLog(
        activity_id="D001",
        user_id="U001",
        action="demand_created",
        demand_number=1001,
        demand_type="Normal",
        equipment_code=501,
        equipment="Compressor",
        financial_year="2025-26",
        store_id="S001",
        changes=[ChangeDetail(field_name="status", old_value="pending", new_value="approved")]
    )
    assert log.demand_number == 1001
    assert log.financial_year == "2025-26"
    assert log.action == "demand_created"
    assert isinstance(log.timestamp, datetime)


# ----------------- Stock Movement Log -----------------

def test_stock_movement_log_instantiation():
    """Test creating StockMovementLog."""
    log = StockMovementLog(
        activity_id="SM001",
        user_id="U001",
        part_number=202,
        nomenclature="Bearing",
        ledger_page="45B",
        store_id="S001",
        movement_type="in",
        quantity=50,
        stock_category="unsv_stock",
        stock_before=100,
        stock_after=150,
        reason="Replenishment"
    )
    assert log.quantity == 50
    assert log.movement_type == "in"
    assert log.stock_after == 150
    assert log.reason == "Replenishment"


# ----------------- Part Audit Log -----------------

def test_part_audit_log_instantiation():
    """Test PartAuditLog basic fields."""
    log = PartAuditLog(
        activity_id="P001",
        user_id="U001",
        action="part_added",
        part_number=303,
        nomenclature="Gear",
        total_stock=120,
        dues_in=5,
        dues_out=2,
        demanded=10,
        used_in_equipments=[{"equipment": "Engine", "equipment_code": 501, "store_id": "S001"}],
        changes=[ChangeDetail(field_name="total_stock", old_value=100, new_value=120)]
    )
    assert log.part_number == 303
    assert log.total_stock == 120
    assert log.used_in_equipments[0]["equipment"] == "Engine"
    assert isinstance(log.timestamp, datetime)


# ----------------- ChangeDetail -----------------

def test_change_detail_model():
    """Test ChangeDetail model standalone."""
    change = ChangeDetail(field_name="quantity", old_value=10, new_value=15)
    assert change.field_name == "quantity"
    assert change.old_value == 10
    assert change.new_value == 15