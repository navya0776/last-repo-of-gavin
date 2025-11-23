import csv
import os
import asyncio
import sys
from data.models.master_tbl import MasterTable
from data.database import get_db, init_db


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# If later "head" becomes "equipment_name" or something else,
# just change this value:
HEAD_FIELD = "eqpt_name"


def safe_str(value):
    return value.strip() if value not in (None, "", "NULL") else None


async def import_master_table_csv(csv_path: str):
    async for session in get_db():
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            records = []

            for row in reader:

                record = MasterTable(
                    Ledger_code=safe_str(row.get("L_CODE")),
                    eqpt_code=safe_str(row.get("E_CODE")),
                    ledger_name=safe_str(row.get("L_NAME")),
                )

                # Dynamically assign head/equipment_name
                setattr(record, HEAD_FIELD, safe_str(row.get("E_NAME")))

                records.append(record)

            session.add_all(records)
            await session.commit()

        print(f"✅ Imported {len(records)} MasterTable records successfully.")


async def main():
    await init_db()
    CSV_PATH = os.path.join(
        os.path.dirname(__file__),

        "csv/scripts/msteqpt.csv"  # replace with your file name
    )
    await import_master_table_csv(CSV_PATH)


asyncio.run(main())
