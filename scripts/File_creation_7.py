import os
import pandas as pd
from datetime import datetime
from typing import List

# -------- USER CONFIG --------
INPUT_FOLDER = "migrations/prov"
OUTPUT_FOLDER = "migrations/provision"

# This is a general filter file that reads all the files in a directory and filter them in the basis of date that are mentioned in DATE_COLUMNS 
# If the files contain many date col then you can add all of them 
# The script will only filter those rows and add them to the file that contains the date above the CUTOFF_DATE in any of the date_col 


# input the col that need to be applied filter on 
DATE_COLUMNS: List[str] = [
    "P_STOCK_DT",
    "DEM_DT",
    "IV_DT1",
    "IV_DT2",
    "IV_DT3",
    "DEP_CTRLDT",
    "SO_DT",
] 



CUTOFF_DATE = datetime(2023, 1, 1)  # cutoff is exclusive (>) — change to >= if you want inclusive
CHUNKSIZE = 100_000
# -----------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def process_file(file_path: str, out_path: str, date_cols: List[str]):
    fname = os.path.basename(file_path)
    print(f"\nProcessing: {fname}")

    # read only header
    try:
        df_head = pd.read_csv(file_path, nrows=0)
    except Exception as e:
        print(f" ❌ Failed to read header: {e}")
        return

    # determine which of the requested date columns exist in this file
    existing = [c for c in date_cols if c in df_head.columns]
    if not existing:
        print(f" ❌ Skipped: none of the requested date columns found ({date_cols}).")
        return

    print(f" ✔ Found date columns to check: {existing}")

    # remove old output
    if os.path.exists(out_path):
        os.remove(out_path)

    wrote = False
    total_out = 0

    # iterate in chunks
    for chunk in pd.read_csv(file_path, chunksize=CHUNKSIZE, low_memory=False):
        # convert only the existing date columns to datetimes (coerce invalid -> NaT)
        for col in existing:
            # avoid KeyError if a column disappears between header read and chunk read
            if col in chunk.columns:
                chunk[col] = pd.to_datetime(chunk[col], errors="coerce")
            else:
                # column unexpectedly missing in this chunk — treat as all-NaT
                chunk[col] = pd.NaT

        # build boolean mask: True if ANY of the date columns > cutoff
        mask = chunk[existing].gt(CUTOFF_DATE).any(axis=1)

        filtered = chunk[mask]

        if not filtered.empty:
            if not wrote:
                filtered.to_csv(out_path, index=False, mode="w")
                wrote = True
            else:
                filtered.to_csv(out_path, index=False, mode="a", header=False)
            total_out += len(filtered)

    if wrote:
        print(f" ✔ Saved filtered file: {out_path}   Rows kept: {total_out}")
    else:
        print(" ⚠ No rows matched; no output created.")


def main():
    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".csv")]
    if not files:
        print("No CSV files in input folder.")
        return

    for fname in files:
        in_path = os.path.join(INPUT_FOLDER, fname)
        out_path = os.path.join(OUTPUT_FOLDER, fname)
        process_file(in_path, out_path, DATE_COLUMNS)


if __name__ == "__main__":
    main()
