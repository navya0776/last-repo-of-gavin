import pytest

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
        d_e_l="L",
    )
    assert details.part_number == 101
