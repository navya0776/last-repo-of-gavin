import pandas as pd
import os

# -----------------------------
# CONFIG
# -----------------------------
main_file = "migrations/master/mstcds.csv"             # CSV where master_id must be added
mapping_file = "migrations/msteqpt_processed.csv"             # CSV containing master_id + Ledger_code
output_file = "migrations/csd_table_output_with_master_id.csv"
removed_file = "migrations/temp/removed_empty_L_CODE_rows.csv"     # rows removed because L_CODE empty
unmatched_file = "migrations/temp/unmatched_L_CODE_rows.csv"       # unmatched after merge (no master_id)

# Column mappings
MAIN_L_CODE = "L_CODE"
MAP_LEDGER_CODE = "Ledger_code"
MAP_MASTER_ID = "master_id"

os.makedirs("migrations/temp", exist_ok=True)

# -----------------------------
# LOAD CSV FILES
# -----------------------------
df_main = pd.read_csv(main_file, dtype=str)
df_map = pd.read_csv(mapping_file, dtype=str)

# -----------------------------
# CLEAN WHITESPACE & NORMALIZE
# -----------------------------
def clean_df(df):
    # strip whitespace on object columns and replace common null-like strings with empty string
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].astype(str).str.strip()
            # keep genuine NaN as NaN
            df[c] = df[c].replace({"nan": None, "None": None})
    return df

df_main = clean_df(df_main)
df_map = clean_df(df_map)

# -----------------------------
# REMOVE ROWS WITH EMPTY L_CODE
# -----------------------------
# Consider empty, None, "NULL" (case-insensitive) as empty
def is_nonempty(val):
    if val is None:
        return False
    if isinstance(val, str):
        v = val.strip()
        if v == "":
            return False
        if v.upper() == "NULL":
            return False
    return True

mask_nonempty = df_main[MAIN_L_CODE].apply(is_nonempty)
removed_rows = df_main[~mask_nonempty].copy()

# Save removed rows for review
if not removed_rows.empty:
    removed_rows.to_csv(removed_file, index=False)
    print(f"Removed {len(removed_rows)} rows with empty {MAIN_L_CODE} -> saved to: {removed_file}")
else:
    # make sure no stale file lying around
    if os.path.exists(removed_file):
        try:
            os.remove(removed_file)
        except Exception:
            pass
    print(f"No empty {MAIN_L_CODE} rows found.")

# Keep only rows where L_CODE is non-empty
df_main = df_main[mask_nonempty].copy()

# -----------------------------
# MERGE USING ONLY L_CODE
# -----------------------------
df_merged = df_main.merge(
    df_map[[MAP_LEDGER_CODE, MAP_MASTER_ID]],
    left_on=MAIN_L_CODE,
    right_on=MAP_LEDGER_CODE,
    how="left"
)

# -----------------------------
# FIND UNMATCHED ROWS
# -----------------------------
unmatched = df_merged[df_merged[MAP_MASTER_ID].isna()].copy()
if not unmatched.empty:
    unmatched.to_csv(unmatched_file, index=False)
    print(f"Unmatched rows (no {MAP_MASTER_ID}) saved to: {unmatched_file} (count: {len(unmatched)})")
else:
    if os.path.exists(unmatched_file):
        try:
            os.remove(unmatched_file)
        except Exception:
            pass
    print("All values matched successfully (no unmatched rows).")

# -----------------------------
# MOVE master_id COLUMN TO FRONT
# -----------------------------
cols = [MAP_MASTER_ID] + [c for c in df_merged.columns if c != MAP_MASTER_ID]
df_merged = df_merged[cols]

# -----------------------------
# SAVE OUTPUT CSV
# -----------------------------
df_merged.to_csv(output_file, index=False)
print(f"Output saved to: {output_file}")

# -----------------------------
# PRINT SUMMARY
# -----------------------------
print("\nSUMMARY:")
print(f" - Total input rows (after removing empty {MAIN_L_CODE}): {len(df_main)}")
print(f" - Rows removed due to empty {MAIN_L_CODE}: {len(removed_rows)}")
print(f" - Total unmatched rows (no {MAP_MASTER_ID}): {len(unmatched)}")
