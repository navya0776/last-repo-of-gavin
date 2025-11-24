import os
import pandas as pd
from datetime import datetime

INPUT_FOLDER = "migrations/master"
OUTPUT_FOLDER = "migrations/filtered_job_csvs"

JOBNO_COLUMN = "JOB_NO"
REQUIRED_COLS = [JOBNO_COLUMN]   # JOB_DT is detected dynamically

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

cutoff_date = datetime(2020, 1, 1)

def find_job_dt_column(columns):
    """
    Detect the JOB DATE column even if named differently:
    JOB_DT, job_dt, job dt, jobdate, JOB-DT, etc.
    """
    cleaned = [c.strip() for c in columns]

    for col in cleaned:
        cname = col.replace(" ", "").replace("-", "").replace("_", "").lower()
        if "job" in cname and ("dt" in cname or "date" in cname):
            return col

    return None


for filename in os.listdir(INPUT_FOLDER):
    if not filename.lower().endswith(".csv"):
        continue

    file_path = os.path.join(INPUT_FOLDER, filename)
    print(f"\nProcessing: {filename}")

    df = pd.read_csv(file_path)

    #------------------------------------------
    # 1️⃣ Find JOB_DT column automatically
    #------------------------------------------
    date_col = find_job_dt_column(df.columns)

    if not date_col:
        print("❌ Skipped: No JOB_DT-style column found.")
        continue

    #------------------------------------------
    # 2️⃣ Ensure JOB_NO exists
    #------------------------------------------
    if JOBNO_COLUMN not in df.columns:
        print(f"❌ Skipped: Missing required column '{JOBNO_COLUMN}'.")
        continue

    print(f"✔ Using date column: {date_col}")

    #------------------------------------------
    # 3️⃣ Convert date safely
    #------------------------------------------
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    #------------------------------------------
    # 4️⃣ Filter rows >= 2023-01-01
    #------------------------------------------
    df_filtered = df[df[date_col] >= cutoff_date]

    #------------------------------------------
    # 5️⃣ Find duplicates in JOB_NO
    #------------------------------------------
    dup_jobnos = df_filtered[df_filtered.duplicated(JOBNO_COLUMN, keep=False)][JOBNO_COLUMN].unique()

    if len(dup_jobnos) == 0:
        print(" No duplicate JOB_NO values.")
    else:
        print(" Duplicate JOB_NO values:", dup_jobnos)

    #------------------------------------------
    # 6️⃣ Save filtered file
    #------------------------------------------
    outpath = os.path.join(OUTPUT_FOLDER, f"filtered_{filename}")
    df_filtered.to_csv(outpath, index=False)

    print(f"✔ Saved filtered file to: {outpath}")
