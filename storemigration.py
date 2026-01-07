import asyncio
from sqlalchemy import select, update
from data.database import get_db, init_db
from data.models.ledgers import Ledger, Stores # Ensure MasterTable is imported
from data.models.master_tbl import MasterTable

async def map_store_ids_to_master():
    print("🔄 Starting mapping of Store IDs to Master Table...")

    async for session in get_db():
        try:
            # 1. Find unique Master_id -> store_id mappings from the Ledger
            # We only want rows where both IDs exist
            stmt = (
                select(Ledger.Master_id, Ledger.store_id)
                .where(Ledger.Master_id.isnot(None))
                .where(Ledger.store_id.isnot(None))
                .distinct()
            )
            
            result = await session.execute(stmt)
            mappings = result.all()

            if not mappings:
                print("⚠️ No mappings found in the Ledger table.")
                return

            print(f"found {len(mappings)} unique mappings. Updating Master Table...")

            # 2. Update each MasterTable entry with its assigned store_id
            updated_count = 0
            for master_id, store_id in mappings:
                update_stmt = (
                    update(MasterTable)
                    .where(MasterTable.Master_id == master_id)
                    .values(store_id=store_id)
                )
                await session.execute(update_stmt)
                updated_count += 1

            await session.commit()
            print(f"✔ Successfully updated {updated_count} MasterTable records!")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error during mapping: {e}")

async def main():
    # Make sure the DB is initialized (and the new store_id column exists)
    await init_db() 
    await map_store_ids_to_master()

if __name__ == "__main__":
    asyncio.run(main())