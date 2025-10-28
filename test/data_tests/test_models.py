import pytest
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)
from data.models.legdersAndos import AllStores, AllEquipments, AllParts
from data.models.provisioning import Demand, Details
from data.models.users import RolePermissions, Role, User

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

# -------------------- Tests for Roles and Users --------------------

def test_rolepermissions_schema_valid():
    schema = RolePermissions.model_json_schema()
    assert "properties" in schema
    assert "read" in schema["properties"]
    assert "write" in schema["properties"]
    assert "delete" in schema["properties"]


def test_rolepermissions_instantiation():
    permissions = RolePermissions(read=True, write=False, delete=False)
    assert permissions.read is True
    assert permissions.write is False
    assert permissions.delete is False


def test_role_schema_valid():
    schema = Role.model_json_schema()
    assert "properties" in schema
    assert "role_name" in schema["properties"]
    assert "permissions" in schema["properties"]


def test_role_instantiation():
    permissions = RolePermissions(read=True, write=True, delete=False)
    role = Role(role_name="Manager", permissions=permissions)
    assert role.role_name == "Manager"
    assert role.permissions.read is True
    assert role.permissions.delete is False


def test_user_schema_valid():
    schema = User.model_json_schema()
    assert "properties" in schema
    assert "username" in schema["properties"]
    assert "password" in schema["properties"]
    assert "role" in schema["properties"]


def test_user_instantiation():
    permissions = RolePermissions(read=True, write=True, delete=False)
    role = Role(role_name="Admin", permissions=permissions)
    user = User(username="testuser", password="secure123", role=role)
    assert user.username == "testuser"
    assert user.password == "secure123"
    assert isinstance(user.role, Role)
    assert user.role.role_name == "Admin"
    assert len(user.id) > 0


def test_user_role_permissions_nested():
    permissions = RolePermissions(read=True, write=False, delete=False)
    role = Role(role_name="Viewer", permissions=permissions)
    user = User(username="viewer1", password="pass123", role=role)
    assert user.role.permissions.read is True
    assert user.role.permissions.write is False
    assert user.role.role_name == "Viewer"
