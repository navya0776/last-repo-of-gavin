from pymongo import ASCENDING
from util_functions import clean_json_schema

# Add parent directory to sys.path

from models.provisioning import AP_Demand  # your root model (contains Demand_Details)


# ---------------- UPGRADE ----------------
async def upgrade(db, session=None):
    """
    Creates the All_Demands collection with strict JSON Schema validation
    automatically derived from the AP_Demand Pydantic model.
    """

    existing = await db.list_collection_names()

    if "All_Demands" not in existing:
        # Generate schema directly from Pydantic model
        schema = {
            "$jsonSchema": clean_json_schema(AP_Demand.model_json_schema())
        }

        await db.create_collection(
            "All_Demands",
            validator=schema,
            validationLevel="strict",  # strict validation against model
            validationAction="error",  # prevent invalid data insertion
        )

    # Create useful indexes
    await db["All_Demands"].create_index(
        [("demand_number", ASCENDING)], unique=True
    )
    await db["All_Demands"].create_index(
        [("details.page_number", ASCENDING)]
    )


# ---------------- DOWNGRADE ----------------
async def downgrade(db, session=None):
    """
    Drops the All_Demands collection if it exists.
    """
    existing = await db.list_collection_names()
    if "All_Demands" in existing:
        await db.drop_collection("All_Demands")
