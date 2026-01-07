import csv
import os
from datetime import datetime


# -------------------------
# SAFE CONVERTERS (same as DB behavior)
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
    if not value or value in ("NULL", ""):
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except:
            pass
    return None


# -------------------------
# MAIN CSV PROCESSOR
# -------------------------
def convert_csv_like_db(input_csv, output_csv):

    records = []
    failed = []
    auto_id = 1  # Simulates AUTO_INCREMENT

    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                # ---- Parse fields ----
                record = {
                    "eqpt_id": auto_id,
                    "master_id": safe_int(row.get("master_id")),
                    "eqpt_code": safe_str(row.get("E_CODE")),
                    "demand_no": safe_str(row.get("DEM_NO")),
                    "demand_type": safe_str(row.get("D_TYPE")),
                    "eqpt_name": safe_str(row.get("E_NAME")),
                    "fin_year": safe_str(row.get("FIN_YEAR")),
                    "dem_dt": safe_date(row.get("DEM_DT")),
                    "demand_auth": safe_str(row.get("SCL_PREPAR")),
                    "dem": safe_int(row.get("DEM")),
                    "full_received": safe_int(row.get("FULL_RECD")),
                    "no_eqpt": safe_int(row.get("NO_EQPT")),
                    "part_received": safe_int(row.get("PART_RECD")),
                    "outstanding": safe_int(row.get("OUTS")),
                    "percent_received": safe_float(row.get("PER_RECD")),
                    "is_locked": safe_str(row.get("YN")),
                    "critical": safe_int(row.get("CRITICAL")),
                    "critical_na": safe_int(row.get("CTRL_NA")),
                    "ved": safe_int(row.get("VED")),
                    "ved_full": safe_int(row.get("VED_FULL")),
                    "ved_part": safe_int(row.get("VED_PART")),
                    "ved_outstanding": safe_int(row.get("VED_OUTS")),
                    "ved_percent": safe_float(row.get("VED_PER")),
                    "ved_cri": safe_int(row.get("VED_CRI")),
                    "ved_cri_na": safe_int(row.get("VED_CTRLNA")),
                }

                # -------------------------
                # DATABASE-LIKE VALIDATIONS
                # -------------------------
                required_fields = [
                    "master_id",
                    "eqpt_code",
                    "demand_no",
                    "demand_type",
                    "eqpt_name",
                    "fin_year",
                    "dem_dt",
                ]

                for field in required_fields:
                    if record[field] in (None, ""):
                        raise ValueError(f"Missing mandatory field: {field}")

                if record["demand_type"] not in ("APD", "SPD"):
                    raise ValueError("Invalid demand_type")

                # Passed all validations
                records.append(record)
                auto_id += 1

            except Exception as e:
                failed.append({"row": row, "error": str(e)})

    # -------------------------
    # WRITE FINAL CSV
    # -------------------------
    if records:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)

    print("\n✅ IMPORT COMPLETE")
    print(f"✔ Valid rows written : {len(records)}")
    print(f"❌ Rejected rows     : {len(failed)}")

    if failed:
        print("\n--- REJECTED ROW DETAILS ---")
        for r in failed:
            print(r)


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    INPUT_CSV = "demand_output_with_masterid.csv"
    OUTPUT_CSV = "demand_table_with_indx.csv"

    convert_csv_like_db(INPUT_CSV, OUTPUT_CSV)