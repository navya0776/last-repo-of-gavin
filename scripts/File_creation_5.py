import pandas as pd
import os
import sys

# -----------------------------
# CONFIG
# -----------------------------
main_file = "migrations/master/mstcds.csv"             # CSV where master_id must be added
mapping_file = "migrations/msteqpt_processed.csv"      # CSV containing master_id + Ledger_code
output_file = "migrations/csd_table_output_with_master_id.csv"

# Temp/Audit files
removed_empty_file = "migrations/temp/removed_empty_L_CODE_rows.csv"
removed_dupe_file = "migrations/temp/removed_duplicates.csv"
unmatched_file = "migrations/temp/unmatched_L_CODE_rows.csv"

# Column mappings
MAIN_L_CODE = "L_CODE"          # This matches your image
MAP_LEDGER_CODE = "Ledger_code" # From your mapping file
MAP_MASTER_ID = "master_id"     # From your mapping file

# ---------------------------------------------------------
# UPDATED COLUMNS BASED ON YOUR IMAGE
# ---------------------------------------------------------
MAIN_EQ_NAME = "E_NAME"  # Matches the 'E_NAME' column in your image
MAIN_EQ_CODE = "E_CODE"  # Matches the 'E_CODE' column in your image

os.makedirs("migrations/temp", exist_ok=True)

# -----------------------------
# LOAD CSV FILES
# -----------------------------
print(f"Loading {main_file}...")
df_main = pd.read_csv(main_file, dtype=str)
df_map = pd.read_csv(mapping_file, dtype=str)

# -----------------------------
# CLEAN WHITESPACE & NORMALIZE
# -----------------------------
def clean_df(df):
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].astype(str).str.strip()
            df[c] = df[c].replace({"nan": None, "None": None})
    return df

df_main = clean_df(df_main)
df_map = clean_df(df_map)

# -----------------------------
# REMOVE DUPLICATES
# -----------------------------
# The 3 columns to check for duplicates: E_NAME, L_CODE, E_CODE
subset_cols = [MAIN_EQ_NAME, MAIN_L_CODE, MAIN_EQ_CODE]

# Verify columns exist before proceeding
missing_cols = [c for c in subset_cols if c not in df_main.columns]
if missing_cols:
    print(f"❌ ERROR: Still missing columns: {missing_cols}")
    print(f"   Available columns in file: {df_main.columns.tolist()}")
    sys.exit(1)

print(f"Checking for duplicates based on: {subset_cols}...")
mask_dupes = df_main.duplicated(subset=subset_cols, keep='first')
duplicates_df = df_main[mask_dupes].copy()

if not duplicates_df.empty:
    duplicates_df.to_csv(removed_dupe_file, index=False)
    print(f"Removed {len(duplicates_df)} duplicate rows -> saved to: {removed_dupe_file}")
else:
    if os.path.exists(removed_dupe_file):
        try: os.remove(removed_dupe_file)
        except: pass
    print("No duplicate entries found.")

# Keep only non-duplicates
df_main = df_main[~mask_dupes].copy()

# -----------------------------
# REMOVE ROWS WITH EMPTY L_CODE
# -----------------------------
def is_nonempty(val):
    if val is None: return False
    if isinstance(val, str):
        v = val.strip()
        if v == "" or v.upper() == "NULL": return False
    return True

mask_nonempty = df_main[MAIN_L_CODE].apply(is_nonempty)
removed_rows = df_main[~mask_nonempty].copy()

if not removed_rows.empty:
    removed_rows.to_csv(removed_empty_file, index=False)
    print(f"Removed {len(removed_rows)} rows with empty {MAIN_L_CODE} -> saved to: {removed_empty_file}")
else:
    if os.path.exists(removed_empty_file):
        try: os.remove(removed_empty_file)
        except: pass
    print(f"No empty {MAIN_L_CODE} rows found.")

df_main = df_main[mask_nonempty].copy()

# -----------------------------
# MERGE
# -----------------------------
print("Merging data...")
df_merged = df_main.merge(
    df_map[[MAP_LEDGER_CODE, MAP_MASTER_ID]],
    left_on=MAIN_L_CODE,
    right_on=MAP_LEDGER_CODE,
    how="left"
)

# -----------------------------
# FIND UNMATCHED
# -----------------------------
unmatched = df_merged[df_merged[MAP_MASTER_ID].isna()].copy()
if not unmatched.empty:
    unmatched.to_csv(unmatched_file, index=False)
    print(f"Unmatched rows (no {MAP_MASTER_ID}) saved to: {unmatched_file} (count: {len(unmatched)})")
else:
    if os.path.exists(unmatched_file):
        try: os.remove(unmatched_file)
        except: pass
    print("All values matched successfully.")

# -----------------------------
# OUTPUT
# -----------------------------
cols = [MAP_MASTER_ID] + [c for c in df_merged.columns if c != MAP_MASTER_ID]
df_merged = df_merged[cols]

df_merged.to_csv(output_file, index=False)
print(f"Output saved to: {output_file}")

print("\nSUMMARY:")
print(f" - Rows removed as duplicates: {len(duplicates_df)}")
print(f" - Rows removed due to empty {MAIN_L_CODE}: {len(removed_rows)}")
print(f" - Total unmatched rows: {len(unmatched)}")
print(f" - Final Valid Output rows: {len(df_merged)}")