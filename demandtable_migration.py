import csv
import os
import asyncio
import sys
from datetime import datetime

from data.models.depot_demand import Demand
from data.database import get_db, init_db


# Windows event loop fix (same as your example)
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# -------------------------
# Safe value helpers
# -------------------------
def safe_str(value):
    return value.strip() if value not in (None, "", "NULL") else None


def safe_int(value):
    try:
        return int(value)
    except:
        return None


def safe_float(value):
    try:
        return float(value)
    except:
        return None


def safe_date(value):
    """Expected format: DD/MM/YYYY or YYYY-MM-DD"""
    if not value or value in ("NULL", ""):
        return None

    # Try multiple formats safely
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except:
            pass

    return None  # Could not parse


# -------------------------
# MAIN IMPORT FUNCTION
# -------------------------
async def import_demand_csv(csv_path: str):
    async for session in get_db():

        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            records = []
            failed = []

            for row in reader:
                try:
                    record = Demand(
                        master_id=safe_int(row.get("master_id")),
                        eqpt_code=safe_str(row.get("E_CODE")),
                        demand_no=safe_str(row.get("DEM_NO")),
                        demand_type=safe_str(row.get("D_TYPE")),
                        eqpt_name=safe_str(row.get("E_NAME")),
                        fin_year=safe_str(row.get("FIN_YEAR")),

                        # Newly added fields
                        dem_dt=safe_date(row.get("DEM_DT")),
                        no_eqpt=safe_int(row.get("NO_EQPT")),
                        dem=safe_int(row.get("DEM")),

                        # Existing fields
                        demand_auth=safe_str(row.get("SCL_PREPAR")),
                        full_received=safe_int(row.get("FULL_RECD")),
                        part_received=safe_int(row.get("PART_RECD")),
                        outstanding=safe_int(row.get("OUTS")),
                        percent_received=safe_float(row.get("PER_RECD")),
                        is_locked=safe_str(row.get("YN")),

                        critical=safe_int(row.get("CRITICAL")),
                        critical_na=safe_int(row.get("CTRL_NA")),
                        ved=safe_int(row.get("VED")),
                        ved_full=safe_int(row.get("VED_FULL")),
                        ved_part=safe_int(row.get("VED_PART")),
                        ved_outstanding=safe_int(row.get("VED_OUTS")),
                        ved_percent=safe_float(row.get("VED_PER")),
                        ved_cri=safe_int(row.get("VED_CRI")),
                        ved_cri_na=safe_int(row.get("VED_CTRLNA")),
                    )

                    records.append(record)

                except Exception as e:
                    failed.append({"row": row, "error": str(e)})

            # Commit only successful rows
            session.add_all(records)
            await session.commit()

        print(f"\n✅ Imported {len(records)} Demand records successfully.")
        print(f"❌ Failed rows: {len(failed)}\n")

        # Print failed rows at the end
        if failed:
            print("------ FAILED ROW DETAILS ------")
            for item in failed:
                print(item)
            print("-------------------------------")


# -------------------------
# MAIN ENTRYPOINT
# -------------------------
async def main():
    await init_db()

    CSV_PATH = os.path.join(
        os.path.dirname(__file__),
        "demand_output_with_masterid.csv"   # CHANGE to your file
    )

    await import_demand_csv(CSV_PATH)


asyncio.run(main())