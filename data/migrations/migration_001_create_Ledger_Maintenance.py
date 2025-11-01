from models.ledgers import LedgerMaintenance
from pymongo import ASCENDING
from util_functions import clean_json_schema


# For Motor (async MongoDB driver) or async wrapper that accepts kwargs:
async def upgrade(db, session=None):
    existing = await db.list_collection_names()
    if "LedgerMaintenance" not in existing:
        schema = {
            "$jsonSchema": clean_json_schema(LedgerMaintenance.model_json_schema())
        }

        await db.create_collection(
            "LedgerMaintenance",
            validator=schema,
            validationLevel="strict",  # optional: "off" | "moderate" | "strict"
            validationAction="error",  # optional: "warn" | "error"
        )

    await db["LedgerMaintenance"].create_index(
        [("ledger_page", ASCENDING)], unique=True
    )


async def downgrade(db, session=None):
    await db.drop_collection("LedgerMaintenance")
