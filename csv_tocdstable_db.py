import csv
import os
import asyncio
import sys
from typing import Any

from data.database import get_db, init_db
from data.models.cds import cds_table

# Windows fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# -------------------------
# SAFE HELPERS
# -------------------------

def safe_str(val):
    if val in (None, "", "NULL"):
        return None
    s = str(val).strip()
    return s if s != "" else None


def safe_int(val):
    try:
        if val in (None, "", "NULL"):
            return None
        return int(str(val).strip())
    except:
        return None


# -------------------------
# COLUMN MAP
# -------------------------

CSV_MAP = {
    "MASTER_ID": "Master_id",
    "L_CODE": "ledger_code",
    "E_CODE": "eqpt_code",
    "E_NAME": "equipment_name",
    "F_HEAD": "head",
    "GROUP": "grp",
    # "L_NAME": ignored (not present in ORM)
}


def norm(key):
    return "".join(c for c in str(key).upper() if c.isalnum() or c == "_")


# -------------------------
# IMPORTER
# -------------------------

async def import_cdstable_csv(csv_path, session, failed):
    print("📄 Importing:", os.path.basename(csv_path))

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            print("❗ No headers in CSV:", csv_path)
            return

        # normalize headers
        header_map = {norm(h): h for h in reader.fieldnames}

        for idx, row in enumerate(reader, start=1):
            try:
                data = {}

                # ----- MAP CSV → ORM -----
                for csv_col_norm, orm_field in CSV_MAP.items():
                    if csv_col_norm not in header_map:
                        continue

                    raw_val = row.get(header_map[csv_col_norm])

                    if orm_field == "Master_id":
                        data[orm_field] = safe_int(raw_val)
                    else:
                        data[orm_field] = safe_str(raw_val)

                # Require master_id
                if not data.get("Master_id"):
                    raise ValueError("Missing master_id")

                # Create ORM object
                record = cds_table(**data)
                session.add(record)

            except Exception as e:
                failed.append({
                    "file": csv_path,
                    "row": idx,
                    "error": str(e),
                    "data": row
                })

        # Commit after file finished
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            failed.append({
                "file": csv_path,
                "row": "commit",
                "error": str(e)
            })


async def import_single_file(csv_path):
    failed = []

    async for session in get_db():
        await import_cdstable_csv(csv_path, session, failed)

    print("\n✔ Completed Import")
    print("❗ Failed rows:", len(failed))
    if failed:
        for r in failed[:20]:
            print(r)


async def main():
    await init_db()

    # ⚠️ CHANGE PATH HERE
    csv_path = os.path.join(
        os.path.dirname(__file__),
        "csd_table_output_with_master_id.csv"
    )

    await import_single_file(csv_path)


if __name__ == "__main__":
    asyncio.run(main())
