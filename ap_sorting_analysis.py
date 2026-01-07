import os
import pandas as pd
from datetime import datetime

# ================= CONFIG =================
INPUT_FOLDER = "migrations/prov"

OUTPUT_VALID = "for_Analysis/processed/valid"
OUTPUT_INVALID = "for_Analysis/processed/invalid"

LOG_FILE = "for_Analysis/migration_report.csv"

os.makedirs(OUTPUT_VALID, exist_ok=True)
os.makedirs(OUTPUT_INVALID, exist_ok=True)

# ========================================

def extract_dem_fields(filename):
    """
    Extract DEM_NO and DEM_DT from filename.
    DEM_NO: 1–4 alphanumeric characters
    DEM_DT: last 6 digits in DDMMYY format
    """
    name = os.path.splitext(filename)[0]

    if len(name) < 7:
        return None, None

    dem_no = name[:-6]
    date_part = name[-6:]

    if not (1 <= len(dem_no) <= 4 and dem_no.isalnum()):
        return None, None

    try:
        dem_dt = datetime.strptime(date_part, "%d%m%y").date()
    except:
        return None, None

    return dem_no, dem_dt


# ================= MAIN PROCESS =================

log_rows = []

for file in os.listdir(INPUT_FOLDER):

    if not file.lower().endswith(".csv"):
        continue

    file_path = os.path.join(INPUT_FOLDER, file)

    try:
        df = pd.read_csv(file_path)
    except:
        log_rows.append([file, "", "", "INVALID", "Unreadable CSV"])
        continue

    dem_no = None
    dem_dt = None
    status = "VALID"
    remarks = ""

    # --- Try reading from CSV ---
    if "DEM_NO" in df.columns and df["DEM_NO"].notna().any():
        dem_no = str(df["DEM_NO"].dropna().iloc[0]).strip()

    if "DEM_DT" in df.columns and df["DEM_DT"].notna().any():
        try:
            dem_dt = pd.to_datetime(df["DEM_DT"].dropna().iloc[0]).date()
        except:
            pass

    # --- Fallback to filename ---
    f_dem_no, f_dem_dt = extract_dem_fields(file)

    if not dem_no and f_dem_no:
        dem_no = f_dem_no

    if not dem_dt and f_dem_dt:
        dem_dt = f_dem_dt

    # --- Final validation ---
    if not dem_no or not dem_dt:
        status = "INVALID"
        remarks = "Missing or invalid DEM_NO or DEM_DT"

    # --- Save output ---
    if status == "VALID":
        save_path = os.path.join(OUTPUT_VALID, file)
    else:
        save_path = os.path.join(OUTPUT_INVALID, file)

    df["DEM_NO"] = dem_no
    df["DEM_DT"] = dem_dt
    df.to_csv(save_path, index=False)

    log_rows.append([file, dem_no, dem_dt, status, remarks])

# ================= LOG FILE =================

log_df = pd.DataFrame(
    log_rows,
    columns=["FILE", "DEM_NO", "DEM_DT", "STATUS", "REMARKS"]
)

log_df.to_csv(LOG_FILE, index=False)

print("✅ Processing complete.")
print("📁 VALID →", OUTPUT_VALID)
print("📁 INVALID →", OUTPUT_INVALID)
print("📄 Report:", LOG_FILE)