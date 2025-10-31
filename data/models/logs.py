from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# Define Indian Standard Time (UTC +5:30)
IST = timezone(timedelta(hours=5, minutes=30))


# ------------------------------
# ENUMS
# ------------------------------
class ActionType(str, Enum):
    """Enumeration of all possible actions in the system."""

    # Store actions
    STORE_CREATED = "store_created"
    STORE_UPDATED = "store_updated"
    STORE_DELETED = "store_deleted"

    # Ledger actions
    LEDGER_CREATED = "ledger_created"
    LEDGER_UPDATED = "ledger_updated"
    LEDGER_DELETED = "ledger_deleted"
    LEDGER_ENTRY_ADDED = "ledger_entry_added"
    LEDGER_ENTRY_MODIFIED = "ledger_entry_modified"

    # Equipment actions
    EQUIPMENT_ADDED = "equipment_added"
    EQUIPMENT_UPDATED = "equipment_updated"
    EQUIPMENT_REMOVED = "equipment_removed"

    # Stock actions
    STOCK_ADDED = "stock_added"
    STOCK_REDUCED = "stock_reduced"
    STOCK_TRANSFERRED = "stock_transferred"
    STOCK_ADJUSTED = "stock_adjusted"
    UNSV_STOCK_UPDATED = "unsv_stock_updated"
    REP_STOCK_UPDATED = "rep_stock_updated"
    SERV_STOCK_UPDATED = "serv_stock_updated"
    CDS_STOCK_UPDATED = "cds_stock_updated"

    # Demand actions
    DEMAND_CREATED = "demand_created"
    DEMAND_UPDATED = "demand_updated"
    DEMAND_APPROVED = "demand_approved"
    DEMAND_REJECTED = "demand_rejected"
    DEMAND_FULFILLED = "demand_fulfilled"
    DEMAND_PARTIALLY_FULFILLED = "demand_partially_fulfilled"
    DEMAND_DELETED = "demand_deleted"
    SUB_DEMAND_ADDED = "sub_demand_added"
    SUB_DEMAND_UPDATED = "sub_demand_updated"

    # Part actions
    PART_ADDED = "part_added"
    PART_UPDATED = "part_updated"
    PART_REMOVED = "part_removed"

    # Dues actions
    DUES_IN_ADDED = "dues_in_added"
    DUES_IN_RECEIVED = "dues_in_received"
    DUES_IN_UPDATED = "dues_in_updated"

    # Consumption actions
    CONSUMPTION_UPDATED = "consumption_updated"

    # User actions
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    USER_PASSWORD_CHANGED = "user_password_changed"
    USER_PASSWORD_RESET = "user_password_reset"
    USER_ROLE_CHANGED = "user_role_changed"
    USER_PERMISSIONS_UPDATED = "user_permissions_updated"

    # Role and Permission actions
    ROLE_CREATED = "role_created"
    ROLE_UPDATED = "role_updated"
    ROLE_DELETED = "role_deleted"
    PERMISSION_CREATED = "permission_created"
    PERMISSION_UPDATED = "permission_updated"
    PERMISSION_DELETED = "permission_deleted"

    # Report actions
    REPORT_GENERATED = "report_generated"
    REPORT_EXPORTED = "report_exported"
    REPORT_VIEWED = "report_viewed"

    # System actions
    BACKUP_CREATED = "backup_created"
    BACKUP_RESTORED = "backup_restored"
    SYSTEM_ERROR = "system_error"
    UNAUTHORIZED_ACCESS_ATTEMPT = "unauthorized_access_attempt"


class ResourceType(str, Enum):
    """Type of resource being logged."""

    STORE = "store"
    LEDGER = "ledger"
    EQUIPMENT = "equipment"
    PART = "part"
    DEMAND = "demand"
    STOCK = "stock"
    USER = "user"
    ROLE = "role"
    PERMISSION = "permission"
    REPORT = "report"
    SYSTEM = "system"


# ------------------------------
# BASE MODELS
# ------------------------------
class ChangeDetail(BaseModel):
    """Details of what changed in an update action."""

    field_name: str
    old_value: Any
    new_value: Any


class AuditLog(BaseModel):
    """Base audit log schema for all activities."""

    activity_id: str
    user_id: str
    action: ActionType
    resource_type: ResourceType
    resource_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(IST).isoformat())

    status: str = "success"  # success, failed, pending, unauthorized
    error_message: str | None = None
    session_id: str | None = None


# ------------------------------
# LEDGER AUDIT
# ------------------------------
class LedgerAuditLog(BaseModel):
    """Audit log for ledger-related operations."""

    activity_id: str
    user_id: str
    action: str
    timestamp: str = Field(default_factory=lambda: datetime.now(IST).isoformat())

    ledger_page: str
    ohs_number: int | None = None
    isg_number: int | None = None
    ssg_number: int | None = None
    part_number: int
    nomenclature: str

    store_id: str
    equipment: str | None = None
    equipment_code: int | None = None

    changes: list[ChangeDetail] | None = None
    details: dict[str, Any] = Field(default_factory=dict)
    stock_changes: dict[str, Any] | None = None

    username: str | None = None


# ------------------------------
# DEMAND AUDIT
# ------------------------------
class DemandAuditLog(BaseModel):
    """Audit log for demand operations."""

    activity_id: str
    user_id: str
    action: str
    timestamp: str = Field(default_factory=lambda: datetime.now(IST).isoformat())

    demand_number: int
    demand_type: str
    equipment_code: int
    equipment: str
    financial_year: str

    sub_demand_number: int | None = None
    part_number: int | None = None
    nomenclature: str | None = None

    store_id: str
    location: str | None = None

    number_of_equiment: int | None = None
    total_demand: int | None = None
    quantity_demanded: int | None = None
    recieved: int | None = None
    outstanding: int | None = None

    previous_status: str | None = None
    current_status: str | None = None

    changes: list[ChangeDetail] | None = None
    details: dict[str, Any] = Field(default_factory=dict)

    approved_by: str | None = None
    rejected_by: str | None = None
    rejection_reason: str | None = None

    username: str | None = None
    full_name: str | None = None


# ------------------------------
# STOCK MOVEMENT AUDIT
# ------------------------------
class StockMovementLog(BaseModel):
    """Audit log for stock movement events."""

    activity_id: str
    user_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(IST).isoformat())

    part_number: int
    nomenclature: str
    ledger_page: str

    equipment: str | None = None
    equipment_code: int | None = None
    store_id: str
    location: str | None = None

    movement_type: str  # "in", "out", "transfer", "adjustment"
    quantity: int

    stock_category: str
    stock_before: int
    stock_after: int

    from_location: str | None = None
    to_location: str | None = None

    reason: str
    reference_document: str | None = None

    ohs_number: int | None = None
    isg_number: int | None = None
    ssg_number: int | None = None

    approved_by: str | None = None
    username: str | None = None


# ------------------------------
# PART AUDIT
# ------------------------------
class PartAuditLog(BaseModel):
    """Audit log for part-level operations."""

    activity_id: str
    user_id: str
    action: str
    timestamp: str = Field(default_factory=lambda: datetime.now(IST).isoformat())

    part_number: int
    nomenclature: str

    total_stock: int | None = None
    dues_in: int | None = None
    dues_out: int | None = None
    demanded: int | None = None

    used_in_equipments: list[dict[str, Any]] | None = None
    changes: list[ChangeDetail] | None = None
    details: dict[str, Any] = Field(default_factory=dict)
    username: str | None = None
