import csv
import os
from datetime import datetime


# -------------------------
# SAFE CASTERS (same as DB behavior)
# -------------------------
def safe_int(val):
    try:
        return int(val) if val not in ("", None) else None
    except:
        return None


def safe_float(val):
    try:
        return float(val) if val not in ("", None) else None
    except:
        return None


def safe_str(val):
    return val.strip() if val not in ("", None) else None


def safe_date(val):
    if val in ("", None):
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(val, fmt).date()
        except:
            pass
    return None


# -------------------------
# CSV → ORM FIELD MAPPING
# -------------------------
CSV_TO_ORM = {
    "master_id": "Master_id",
    "store_id": "store_id",
    "L_CODE": "Ledger_code",
    "L_PAGE": "ledger_page",
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
# CORE CSV PROCESSOR
# -------------------------
def convert_ledger_csv(input_folder, output_csv):
    records = []
    auto_id = 1

    for file in os.listdir(input_folder):
        if not file.lower().endswith(".csv"):
            continue

        path = os.path.join(input_folder, file)
        print(f"Processing → {file}")

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                record = {}

                for csv_key, orm_key in CSV_TO_ORM.items():
                    val = row.get(csv_key)

                    if orm_key in (
                        "store_id", "Master_id", "no_off", "scl_auth",
                        "consumption", "Re_ord_lvl", "qty",
                        "br_stock", "dem", "rep_stock", "serv_stock"
                    ):
                        record[orm_key] = safe_int(val)

                    elif orm_key in ("rate", "sale_rate", "dem_val"):
                        record[orm_key] = safe_float(val)

                    elif orm_key in (
                        "br_stock_dt", "p_stock_dt", "r_stock_dt",
                        "stock_dt", "lock_dt", "lpp_dt"
                    ):
                        record[orm_key] = safe_date(val)

                    else:
                        record[orm_key] = safe_str(val)

                # Simulate auto-increment primary key
                record["ledger_id"] = auto_id
                auto_id += 1

                records.append(record)

    # -------------------------
    # WRITE OUTPUT CSV
    # -------------------------
    if records:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)

    print("\n✅ CSV GENERATED SUCCESSFULLY")
    print(f"Total records written: {len(records)}")


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    INPUT_FOLDER = "migrations/ledgers"
    OUTPUT_FILE = "ledger_with_indx.csv"

    convert_ledger_csv(INPUT_FOLDER, OUTPUT_FILE)