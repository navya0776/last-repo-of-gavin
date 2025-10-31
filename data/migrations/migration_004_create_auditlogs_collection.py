from pymongo import ASCENDING
from util_functions import clean_json_schema

from models.logs import (
    AuditLog,
    LedgerAuditLog,
    DemandAuditLog,
    StockMovementLog,
    PartAuditLog,
)


async def upgrade(db, session=None):
    """Creates collections for audit log models with schema validation and indexes."""
    existing = await db.list_collection_names()

    # General audit logs
    if "Audit_Logs" not in existing:
        await db.create_collection(
            "Audit_Logs",
            validator={"$jsonSchema": clean_json_schema(AuditLog.model_json_schema())},
        )
        await db["Audit_Logs"].create_index([("activity_id", ASCENDING)], unique=True)
        await db["Audit_Logs"].create_index([("user_id", ASCENDING)])
        await db["Audit_Logs"].create_index([("action", ASCENDING)])
        await db["Audit_Logs"].create_index([("timestamp", ASCENDING)])

    # Ledger audit logs
    if "Ledger_Audit_Logs" not in existing:
        await db.create_collection(
            "Ledger_Audit_Logs",
            validator={
                "$jsonSchema": clean_json_schema(LedgerAuditLog.model_json_schema())
            },
        )
        await db["Ledger_Audit_Logs"].create_index(
            [("activity_id", ASCENDING)], unique=True
        )
        await db["Ledger_Audit_Logs"].create_index([("ledger_page", ASCENDING)])
        await db["Ledger_Audit_Logs"].create_index([("store_id", ASCENDING)])
        await db["Ledger_Audit_Logs"].create_index([("timestamp", ASCENDING)])

    # Demand audit logs
    if "Demand_Audit_Logs" not in existing:
        await db.create_collection(
            "Demand_Audit_Logs",
            validator={
                "$jsonSchema": clean_json_schema(DemandAuditLog.model_json_schema())
            },
        )
        await db["Demand_Audit_Logs"].create_index(
            [("activity_id", ASCENDING)], unique=True
        )
        await db["Demand_Audit_Logs"].create_index([("demand_number", ASCENDING)])
        await db["Demand_Audit_Logs"].create_index([("store_id", ASCENDING)])
        await db["Demand_Audit_Logs"].create_index([("timestamp", ASCENDING)])

    # Stock movement logs
    if "Stock_Movement_Logs" not in existing:
        await db.create_collection(
            "Stock_Movement_Logs",
            validator={
                "$jsonSchema": clean_json_schema(StockMovementLog.model_json_schema())
            },
        )
        await db["Stock_Movement_Logs"].create_index(
            [("activity_id", ASCENDING)], unique=True
        )
        await db["Stock_Movement_Logs"].create_index([("part_number", ASCENDING)])
        await db["Stock_Movement_Logs"].create_index([("movement_type", ASCENDING)])
        await db["Stock_Movement_Logs"].create_index([("store_id", ASCENDING)])
        await db["Stock_Movement_Logs"].create_index([("timestamp", ASCENDING)])

    # Part audit logs
    if "Part_Audit_Logs" not in existing:
        await db.create_collection(
            "Part_Audit_Logs",
            validator={
                "$jsonSchema": clean_json_schema(PartAuditLog.model_json_schema())
            },
        )
        await db["Part_Audit_Logs"].create_index(
            [("activity_id", ASCENDING)], unique=True
        )
        await db["Part_Audit_Logs"].create_index([("part_number", ASCENDING)])
        await db["Part_Audit_Logs"].create_index([("timestamp", ASCENDING)])


async def downgrade(db, session=None):
    """Drops all audit log collections."""
    await db.drop_collection("Audit_Logs")
    await db.drop_collection("Ledger_Audit_Logs")
    await db.drop_collection("Demand_Audit_Logs")
    await db.drop_collection("Stock_Movement_Logs")
    await db.drop_collection("Part_Audit_Logs")
