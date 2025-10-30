import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.users import User  # adjust path if needed
from pymongo import ASCENDING
from util_functions import clean_json_schema


async def upgrade(db, session=None):
    """
    Migration script to create the Users collection with JSON schema validation
    and indexes for efficient lookups.
    """
    existing = await db.list_collection_names()

    if "Users" not in existing:
        await db.create_collection(
            "Users",
        )

        # Create unique index for username to ensure no duplicates
        await db["Users"].create_index("username", unique=True)

        # You can add more indexes if needed (e.g., role.role_name)
        await db["Users"].create_index([("role.role_name", ASCENDING)])


async def downgrade(db, session=None):
    """
    Downgrade script to drop the Users collection if rollback is needed.
    """
    await db.drop_collection("Users")
