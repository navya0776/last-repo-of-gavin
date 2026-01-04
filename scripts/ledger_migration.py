import csv
import os
import asyncio
import sys
from datetime import datetime

from data.models.ledgers import Ledger
from data.database import get_db, init_db


# Windows fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# -------------------------
# SAFE HELPERS
# -------------------------
def safe_int(val):
    try:
        return int(val) if val not in (None, "", "NULL") else None
    except:
        return None


def safe_float(val):
    try:
        return float(val) if val not in (None, "", "NULL") else None
    except:
        return None


def safe_str(val):
    return val.strip() if val not in (None, "", "NULL") else None


def safe_date(val):
    if val in (None, "", "NULL"):
        return None

    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(val, fmt).date()
        except:
            pass

    return None


# -------------------------
# CSV → ORM mapping
# -------------------------
CSV_TO_ORM = {
    "master_id": "Master_id",
    "store_id": "store_id",
    "L_CODE": "Ledger_code",
    "L_PAGE": "ledger_page",     # <-- CORRECT — now we use L_PAGE from CSV

    "SCL_NO": "ohs_number",
    "ISG_NO": "isg_number",
    "SSG_NO": "ssg_number",
    "PART_NO": "part_number",
    "NOMEN": "nomenclature",
    "A_U": "a_u",
    "NO_OFF": "no_off",
    "SCL_AUTH": "scl_auth",
    "CONS": "consumption",
    "BIN_NO": "bin_number",
    "GROUP": "group",
    "PRICE": "rate",
    "COMPONENT": "Assy_Comp",
    "R_LEVEL": "Re_ord_lvl",

    "P_STOCK": "serv_stock",
    "R_STOCK": "rep_stock",

    "MSC": "msc",
    "VED": "ved",
    "IN_HOUSE": "in_house",
    "LPP": "lpp",
    "LPP_DT": "lpp_dt",

    "BR_STOCK": "br_stock",
    "BR_STOCKDT": "br_stock_dt",
    "CAB": "cab",
    "DEM": "dem",
    "DEM_VAL": "dem_val",
    "LOCK_DT": "lock_dt",
    "NPART_NO": "npart_no",
    "NSCL_NO": "nscl_no",
    "OLD_PAGE": "old_page",
    "P_STOCK_DT": "p_stock_dt",
    "QTY": "qty",
    "R_STOCK_DT": "r_stock_dt",
    "SALE_RATE": "sale_rate",
    "SL": "sl",
    "SPART_NO": "spart_no",
    "STOCK_DT": "stock_dt",
    "YN": "yn",
}


# -------------------------
# Import ONE CSV
# -------------------------
async def import_ledger_csv(csv_path: str, session, failed_rows: list):
    print(f"📄 Importing: {os.path.basename(csv_path)}")

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                data = {}

                for key, orm_field in CSV_TO_ORM.items():
                    if key not in row:
                        continue

                    value = row[key]

                    # int fields
                    if orm_field in (
                        "store_id", "Master_id", "no_off", "scl_auth",
                        "consumption", "Re_ord_lvl", "qty", "br_stock",
                        "dem", "rep_stock", "serv_stock"
                    ):
                        data[orm_field] = safe_int(value)

                    # float fields
                    elif orm_field in ("rate", "sale_rate", "dem_val"):
                        data[orm_field] = safe_float(value)

                    # date fields
                    elif orm_field in (
                        "br_stock_dt", "p_stock_dt", "r_stock_dt",
                        "stock_dt", "lock_dt", "lpp_dt"
                    ):
                        data[orm_field] = safe_date(value)

                    # string fields
                    else:
                        data[orm_field] = safe_str(value)

                # Required field
                data["unsv_stock"] = 0

                record = Ledger(**data)
                session.add(record)

            except Exception as e:
                failed_rows.append({
                    "file": csv_path,
                    "row": row,
                    "error": str(e)
                })

    await session.commit()


# -------------------------
# Import ALL CSVs in folder
# -------------------------
async def import_all_ledgers(folder_path: str):
    failed_rows = []

    async for session in get_db():
        for file in os.listdir(folder_path):
            if file.lower().endswith(".csv"):
                await import_ledger_csv(
                    os.path.join(folder_path, file),
                    session,
                    failed_rows
                )

    print("\n--------------------------------------")
    print("✔ COMPLETED LEDGER CSV IMPORT")
    print("--------------------------------------")
    print(f"❗ Failed rows: {len(failed_rows)}")

    if failed_rows:
        print("\n--- FAILED ROWS ---")
        for r in failed_rows:
            print(r)


# -------------------------
# MAIN
# -------------------------
async def main():
    await init_db()

    folder = os.path.join(
        os.path.dirname(__file__),
        "../migrations/ledgers"
    )

    await import_all_ledgers(folder)


if __name__ == "__main__":
    asyncio.run(main())
