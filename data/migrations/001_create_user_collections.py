"""
Migration 001: create `users` collection and unique index on email.
Run by data/run_migrations.py
"""

from pymongo import ASCENDING


async def upgrade(db, session=None):
    """
    Apply this migration.
    Creates a 'users' collection and adds a unique index on 'email'.
    """
    print("Applying migration 001_create_users_collection...")
    users = db.get_collection("users")

    # Create collection explicitly (optional)
    existing_collections = await db.list_collection_names(session=session)
    if "users" not in existing_collections:
        await db.create_collection("users", session=session)

    # Add unique email index
    await users.create_index(
        [("email", ASCENDING)], unique=True, name="email_unique_idx", session=session
    )
    print("Created 'users' collection with unique email index.")


async def downgrade(db, session=None):
    """
    Rollback this migration.
    Drops the 'users' collection.
    """
    print("Reverting migration 001_create_users_collection...")
    existing_collections = await db.list_collection_names(session=session)
    if "users" in existing_collections:
        await db.drop_collection("users", session=session)
        print("Dropped 'users' collection.")
