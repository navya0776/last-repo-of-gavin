import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pymongo import ASCENDING
from models.legdersAndos import AllStores, AllEquiments, AllParts
from util_functions import clean_json_schema

async def upgrade(db, session=None):
    existing = await db.list_collection_names()

    if "All_Stores" not in existing:
        await db.create_collection(
            "All_Stores",
            validator={"$jsonSchema": clean_json_schema(AllStores.model_json_schema())}
        )
        await db["All_Stores"].create_index("store_id", unique=True)

    if "All_Equipments" not in existing:
        await db.create_collection(
            "All_Equipments",
            validator={"$jsonSchema": clean_json_schema(AllEquiments.model_json_schema())}
        )
        await db["All_Equiments"].create_index("equipment_code", unique=True)

    
    if "All_Parts" not in existing:
        await db.create_collection(
            "All_Parts",
            validator={"$jsonSchema": clean_json_schema(AllParts.model_json_schema())}
        )
        await db["All_Parts"].create_index("part_number", unique=True)

async def downgrade(db, session=None):
    await db.drop_collection("All_Stores")
    await db.drop_collection("All_Equiments")
    await db.drop_collection("All_Parts")