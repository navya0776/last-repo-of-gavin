# models/audit.py
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, JSON, Enum as SAEnum)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))


# --- Define string enums (mirror values from your logs.py) ---
from enum import Enum


class ActionTypeEnum(str, Enum):
    STORE_CREATED = "store_created"
    STORE_UPDATED = "store_updated"
    STORE_DELETED = "store_deleted"
    LEDGER_CREATED = "ledger_created"
    LEDGER_UPDATED = "ledger_updated"
    LEDGER_DELETED = "ledger_deleted"
    LEDGER_ENTRY_ADDED = "ledger_entry_added"
    LEDGER_ENTRY_MODIFIED = "ledger_entry_modified"
    EQUIPMENT_ADDED = "equipment_added"
    EQUIPMENT_UPDATED = "equipment_updated"
    EQUIPMENT_REMOVED = "equipment_removed"
    STOCK_ADDED = "stock_added"
    STOCK_REDUCED = "stock_reduced"
    STOCK_TRANSFERRED = "stock_transferred"
    STOCK_ADJUSTED = "stock_adjusted"
    UNSV_STOCK_UPDATED = "unsv_stock_updated"
    REP_STOCK_UPDATED = "rep_stock_updated"
    SERV_STOCK_UPDATED = "serv_stock_updated"
    CDS_STOCK_UPDATED = "cds_stock_updated"
    DEMAND_CREATED = "demand_created"
    DEMAND_UPDATED = "demand_updated"
    DEMAND_APPROVED = "demand_approved"
    DEMAND_REJECTED = "demand_rejected"
    DEMAND_FULFILLED = "demand_fulfilled"
    DEMAND_PARTIALLY_FULFILLED = "demand_partially_fulfilled"
    DEMAND_DELETED = "demand_deleted"
    SUB_DEMAND_ADDED = "sub_demand_added"
    SUB_DEMAND_UPDATED = "sub_demand_updated"
    PART_ADDED = "part_added"
    PART_UPDATED = "part_updated"
    PART_REMOVED = "part_removed"
    DUES_IN_ADDED = "dues_in_added"
    DUES_IN_RECEIVED = "dues_in_received"
    DUES_IN_UPDATED = "dues_in_updated"
    CONSUMPTION_UPDATED = "consumption_updated"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    USER_PASSWORD_CHANGED = "user_password_changed"
    USER_PASSWORD_RESET = "user_password_reset"
    USER_ROLE_CHANGED = "user_role_changed"
    USER_PERMISSIONS_UPDATED = "user_permissions_updated"
    ROLE_CREATED = "role_created"
    ROLE_UPDATED = "role_updated"
    ROLE_DELETED = "role_deleted"
    PERMISSION_CREATED = "permission_created"
    PERMISSION_UPDATED = "permission_updated"
    PERMISSION_DELETED = "permission_deleted"
    REPORT_GENERATED = "report_generated"
    REPORT_EXPORTED = "report_exported"
    REPORT_VIEWED = "report_viewed"
    BACKUP_CREATED = "backup_created"
    BACKUP_RESTORED = "backup_restored"
    SYSTEM_ERROR = "system_error"
    UNAUTHORIZED_ACCESS_ATTEMPT = "unauthorized_access_attempt"


class ResourceTypeEnum(str, Enum):
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
    CDS = "cds"
    VENDOR = "vendor"
    LPR = "lpr"
    FLOATING_INDENT = "floating_indent"
    DEPOT_DEMAND = "depot_demand"        # APDemand in your screenshot
    INDENT = "indent"
    JOB = "job"  


# --- Core audit log table (generic) ---
class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_id: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(120),ForeignKey("users.username"),nullable=False,)
    action: Mapped[ActionTypeEnum] = mapped_column(SAEnum(ActionTypeEnum, native_enum=False), nullable=False)
    resource_type: Mapped[ResourceTypeEnum] = mapped_column(SAEnum(ResourceTypeEnum, native_enum=False), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(120), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,default=lambda: datetime.now(IST))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="success")
    error_message: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
    session_id: Mapped[str] = mapped_column(String(120), nullable=False)
