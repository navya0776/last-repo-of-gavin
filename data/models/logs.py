from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta
from enum import Enum

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
    """Type of resource being logged"""

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


class ChangeDetail(BaseModel):
    """Details of what changed in an update action"""

    field_name: str
    old_value: Any
    new_value: Any


class AuditLog(BaseModel):
    """Main audit log model - aligned with your existing schemas"""

    activity_id: str  # Unique identifier for the log entry
    user_id: str  # From User model
    action: ActionType  # Type of action performed (using ActionType enum values)
    resource_type: (
        ResourceType  # Type of resource affected (using ResourceType enum values)
    )
    resource_id: str  # ID of the affected resource
    timestamp: str = Field(default_factory=lambda: datetime.now(IST).isoformat())

    # Status and outcome
    status: str = "success"  # success, failed, pending, unauthorized
    error_message: str | None = None  # If status is failed

    # Request context
    session_id: str | None = None


class LedgerAuditLog(BaseModel):
    """Specialized audit log for ledger operations - aligned with LedgerMaintenance"""

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

    # Store context
    store_id: str
    equipment: str | None = None
    equipment_code: int | None = None

    changes: list[ChangeDetail] | None = None
    details: dict[str, Any] = Field(default_factory=dict)
    stock_changes: dict[str, Any] | None = None

    username: str | None = None


class DemandAuditLog(BaseModel):
    """Specialized audit log for demand operations - aligned with Demand and Details"""

    activity_id: str
    user_id: str
    action: str
    timestamp: str = Field(default_factory=lambda: datetime.now(IST).isoformat())

    demand_number: int
    demand_type: str
    equipment_code: int
    equipment: str
    financial_year: str

    # Sub-demand (if applicable) - from Details model
    sub_demand_number: int | None = None
    part_number: int | None = None
    nomenclature: str | None = None

    # Store context
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


class StockMovementLog(BaseModel):
    """Specialized log for stock movements - aligned with LedgerMaintenance stock fields"""

    activity_id: str
    user_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(IST).isoformat())

    part_number: int
    nomenclature: str
    ledger_page: str

    # Equipment context - from StoreLedgerDocument
    equipment: str | None = None
    equipment_code: int | None = None

    # Store context - from AllStores
    store_id: str
    location: str | None = None

    # Movement type
    movement_type: str  # "in", "out", "transfer", "adjustment"
    quantity: int

    # Stock category and changes - aligned with LedgerMaintenance fields
    stock_category: str  # "unsv_stock", "rep_stock", "serv_stock", "cds_unsv_stock", "cds_rep_stock", "cds_serv_stock"
    stock_before: int
    stock_after: int

    # Transfer details (if applicable)
    from_location: str | None = None
    to_location: str | None = None

    # Context
    reason: str
    reference_document: str | None = None  # Demand number, receipt number, etc.

    # OHS/ISG/SSG context from LedgerMaintenance
    ohs_number: int | None = None
    isg_number: int | None = None
    ssg_number: int | None = None

    # Approval
    approved_by: str | None = None

    # User details
    username: str | None = None


class PartAuditLog(BaseModel):
    """Audit log for part-level operations - aligned with AllParts"""

    activity_id: str
    user_id: str
    action: str
    timestamp: str = Field(default_factory=lambda: datetime.now(IST).isoformat())

    part_number: int
    nomenclature: str

    total_stock: Optional[int] = None
    dues_in: Optional[int] = None
    dues_out: Optional[int] = None
    demanded: Optional[int] = None

    used_in_equipments: Optional[List[Dict[str, Any]]] = None
    changes: Optional[List[ChangeDetail]] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    username: Optional[str] = None
