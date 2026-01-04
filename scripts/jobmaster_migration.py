# csv_to_jobmaster.py

import csv
import os
import asyncio
import sys
from datetime import datetime
from typing import Any, Union

from data.database import get_db, init_db
from data.models.cds import JobMaster

# Windows event-loop fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# -------------------------
# SAFE HELPERS
# -------------------------

def safe_int(val):
    try:
        if val in (None, "", "NULL"):
            return None
        s = str(val).strip().replace(",", "")
        if s == "":
            return None
        return int(float(s))
    except:
        return None


def safe_float(val):
    try:
        if val in (None, "", "NULL"):
            return None
        s = str(val).strip().replace(",", "")
        if s == "":
            return None
        return float(s)
    except:
        return None


def safe_str(val):
    if val in (None, "", "NULL"):
        return None
    s = str(val).strip()
    return s if s != "" else None


def safe_date(val):
    if val in (None, "", "NULL"):
        return None

    s = str(val).strip()
    if s == "":
        return None

    fmts = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%d.%m.%Y",
    ]

    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt).date()
        except:
            pass

    try:
        return datetime.fromisoformat(s).date()
    except:
        return None


# -------------------------
# BASIC MAPPING (STATIC)
# -------------------------

CSV_BASE_MAP = {
    "PREFIX": "job_prefix",
    "SUFFIX": "job_suffix",
    "JOB_NO": "job_no",
    "JOB_DT": "job_date",
    "EQPT": "eqpt_name",
    "E_CODE": "eqpt_code",
    "MAKE": "make",
    "MODEL": "model",
    "CHASSIS_NO": "ch_no",
    "CHASSISNO": "ch_no",
    "CATALOGUE": "catalogue_ref",
    "SCL_REF": "ohs",
    "NAT_REP": "comit_type",
    "QTY": "no_eqpt",
    "QTY_COMP": "no_comp",
    "DT_COMP": "date_comp",
    "DEM": "item_dem",
    "F_ISS": "full_iss",
    "P_ISS": "part_iss",
    "N_ISS": "nil_iss",
    "ON_LP": "on_LPR",
    "ON_ENQ": "enq_placed",
    "ON_SO": "SO_placed",
    "SO_FULL": "recd_full",
    "SO_PART": "recd_part",
    "SOCAN_NR": "so_nr_cancel",
    "DEMCAN_NR": "cancel_nr",
    "MT_LP": "MT_LP",
    "ENGR_LP": "ENGR_LP",
    "ORD_LP": "ORD_LP",
    "TOTAL_LP": "TOTAL_LP",
    "LP_ACCESS": "LP_access_date",
    "DT_RECD": "dt_received",
    "DT_P_ST": "prod_started",
    "DEPOT": "depot",
    "DEP_WO": "dep_wo",
    "DEP_WODT": "dep_wodate",
    "QTY_COMPLETED": "qty_completed",
    "REMARKS": "remarks",
    "AHQ_SRL": "ahq_srl",
    "CUM_TOT": "cum_tot",
    "LAST_VIR": "VIR_supp",
    "EM_NO": "em_no",    # single engine number field
    "MASTER_ID": "master_id",
}


# -------------------------
# DYNAMIC SERIES (1–12)
# -------------------------

SERIES_CONFIG = [
    ("BA", "em_ba_no_eng", 12, "str"),
    ("ENG", "eng_no", 12, "str"),
    ("ENG_JOB", "eng_job", 12, "str"),
    ("ENG_JDT", "eng_job_date", 12, "date"),
    ("UNIT", "unit", 12, "str"),
    ("SUB_NO", "sub_assy_no", 12, "str"),
    ("SUB_JOB", "sub_assy_job", 12, "str"),
    ("SUB_JDT", "sub_assy_date", 12, "date"),
    ("TABLE_DATE_COMPLETED", "table_date_completed", 12, "date"),
    ("TGT_SRL", "tgt_date", 12, "date"),
    ("TGT", "tgt_date", 12, "date"),
    ("BD_SRL", "bd_srl", 12, "str"),
    ("PROG", "prog", 12, "float"),
    ("GANG_LDR", "gang_ldr", 12, "str"),
]


def norm(k):
    return "".join(c for c in str(k).upper() if c.isalnum() or c == "_")


# -------------------------
# IMPORT ONE CSV
# -------------------------

async def import_jobmaster_csv(csv_path, session, failed):

    print("📄 Importing:", os.path.basename(csv_path))

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            print("❗ No headers found in CSV:", csv_path)
            return

        header_map = {norm(h): h for h in reader.fieldnames}

        for row_index, row in enumerate(reader, start=1):
            try:
                data = {}

                # ------- STATIC MATCHING -------
                for key_norm, orm_field in CSV_BASE_MAP.items():
                    if key_norm in header_map:
                        val = row.get(header_map[key_norm])

                        if orm_field in (
                            "master_id", "no_eqpt", "no_comp", "item_dem",
                            "full_iss", "part_iss", "nil_iss", "cancel_nr",
                            "on_LPR", "enq_placed", "SO_placed",
                            "recd_full", "recd_part", "so_nr_cancel",
                            "MT_LP", "ENGR_LP", "ORD_LP", "TOTAL_LP",
                            "cum_tot", "qty_completed", "VIR_supp"
                        ):
                            data[orm_field] = safe_int(val)

                        elif orm_field in (
                            "LP_access_date", "dep_wodate", "dt_received",
                            "prod_started", "date_comp", "job_date"
                        ):
                            data[orm_field] = safe_date(val)

                        else:
                            data[orm_field] = safe_str(val)

                # ------- SERIES MATCHING -------
                for prefix, orm_base, limit, dtype in SERIES_CONFIG:
                    for i in range(1, limit + 1):
                        csv_key = f"{prefix}{i:02d}"
                        kn = norm(csv_key)

                        if kn in header_map:
                            val = row.get(header_map[kn])
                            field = f"{orm_base}_{i}"

                            if dtype == "int":
                                data[field] = safe_int(val)
                            elif dtype == "float":
                                data[field] = safe_float(val)
                            elif dtype == "date":
                                data[field] = safe_date(val)
                            else:
                                data[field] = safe_str(val)

                # ------- COMPUTE bal_itens -------
                dem = data.get("item_dem")
                full = data.get("full_iss") or 0
                part = data.get("part_iss") or 0
                nil = data.get("nil_iss") or 0

                if dem is not None:
                    data["bal_itens"] = dem - (full + part + nil)

                # ------- CHECK master_id -------
                if not data.get("master_id"):
                    raise ValueError("Missing master_id")

                # ------- TRIM job_no -------
                if "job_no" in data and data["job_no"]:
                    data["job_no"] = str(data["job_no"])[:6]

                # ------- SAVE -------
                record = JobMaster(**data)
                session.add(record)

            except Exception as e:
                failed.append({
                    "file": csv_path,
                    "row": row_index,
                    "error": str(e),
                    "data": row
                })

        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            failed.append({
                "file": csv_path,
                "row": "commit",
                "error": str(e)
            })


# -------------------------
# IMPORT SINGLE FILE
# -------------------------

async def import_single_jobmaster(csv_path):
    failed = []

    async for session in get_db():
        await import_jobmaster_csv(csv_path, session, failed)

    print("\n✔ Completed Import")
    print("❗ Failed rows:", len(failed))
    if failed:
        for r in failed[:20]:
            print(r)


# -------------------------
# MAIN
# -------------------------

async def main():
    await init_db()

    # ⚠️ CHANGE THIS PATH TO YOUR CSV FILE
    csv_path = os.path.join(
        os.path.dirname(__file__),
        "../migrations/jobmaster_with_master_id.csv"
    )

    await import_single_jobmaster(csv_path)


if __name__ == "__main__":
    asyncio.run(main())
