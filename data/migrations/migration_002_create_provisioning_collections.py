import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.provisioning import Demand
from pymongo import ASCENDING
from util_functions import clean_json_schema


async def upgrade(db, session=None):
    existing = await db.list_collection_names()

    if "All_Demands" not in existing:
        await db.create_collection(
            "All_Demands",
            validator={"$jsonSchema": clean_json_schema(Demand.model_json_schema())},
        )
        await db["All_Demands"].create_index("demand_number", unique=True)
        await db["All_Demands"].create_index(
            [("details.ledger_page_number", ASCENDING)]
        )


async def downgrade(db, session=None):
    await db.drop_collection("All_Demands")
