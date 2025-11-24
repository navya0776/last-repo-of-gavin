import asyncio
from sqlalchemy import insert

from data.models.ledgers import Stores
from data.database import get_db, init_db


STORES_TO_INSERT = [
    {"store_id": 1, "store_name": "ENGR STORE"},
    {"store_id": 2, "store_name": "ORDNANCE STORE"},
    {"store_id": 3, "store_name": "KRAZ STORE"},
    {"store_id": 4, "store_name": "EXP STORE"},
    {"store_id": 5, "store_name": "INDG STORE"},
    {"store_id": 6, "store_name": "SCANIA STORE"},
    {"store_id": 7, "store_name": "TATRA STORE"},
    {"store_id": 8, "store_name": "TATA TIPPER"},
    {"store_id": 9, "store_name": "ARV STORE"},
]


async def insert_stores():
    print("📦 Inserting stores...")

    async for session in get_db():
        try:
            stmt = insert(Stores).values(STORES_TO_INSERT)
            await session.execute(stmt)
            await session.commit()

            print("✔ Stores inserted successfully!")
        except Exception as e:
            await session.rollback()
            print("❌ Error inserting stores:", e)


async def main():
    await init_db()
    await insert_stores()


if __name__ == "__main__":
    asyncio.run(main())
