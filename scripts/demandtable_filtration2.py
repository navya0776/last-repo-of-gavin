import pandas as pd
import re

# ================================
# CONFIG
# ================================
MAIN_FILE = "mstprov.csv"
MASTER_FILE = "msteqpt_processed.csv"

OUTPUT_FILE = "demand_output_with_masterid.csv"
REMOVED_STEP4_FILE = "removed_masterid_rows.csv"

# Column names
COL_FIN_YEAR = "FIN_YEAR"
COL_L_CODE = "L_CODE"
COL_E_CODE = "E_CODE"
COL_E_NAME = "E_NAME"
COL_DEM_NO = "DEM_NO"

# ================================
# CLEANING (fix invisible whitespace)
# ================================
WHITESPACE_RE = re.compile(
    r'[\s\u00A0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000\u200B\u200C\u200D\uFEFF]+'
)
def clean_str(val):
    if val is None:
        return ""
    # Remove all special whitespace
    s = WHITESPACE_RE.sub(" ", str(val))
    return s.strip()

# ================================
# LOAD FILES
# ================================
main_df = pd.read_csv(MAIN_FILE, dtype=str)
master_df = pd.read_csv(MASTER_FILE, dtype=str)

# =====================================================
# STEP 1 — FILTER BASED ON FINANCIAL YEAR
# =====================================================
def fin_year_filter(value):
    try:
        start = int(value.split("-")[0])
        return start >= 2022
    except:
        return False

filtered_df = main_df[main_df[COL_FIN_YEAR].apply(fin_year_filter)].copy()

# =====================================================
# STEP 1.5 — FIX NaN FIRST (CRITICAL)
# =====================================================
filtered_df = filtered_df.fillna("")   # <-- This removes all NaN from E_NAME, DEM_NO etc.

# =====================================================
# STEP 2 — CLEAN E_NAME AND DEM_NO
# =====================================================
filtered_df[COL_E_NAME] = filtered_df[COL_E_NAME].apply(clean_str)
filtered_df[COL_DEM_NO] = filtered_df[COL_DEM_NO].apply(clean_str)

# =====================================================
# STEP 3 — REMOVE EMPTY E_NAME
# =====================================================
filtered_df = filtered_df[
    filtered_df[COL_E_NAME] != ""
].copy()

# =====================================================
# STEP 4 — REMOVE EMPTY DEM_NO
# =====================================================
filtered_df = filtered_df[
    filtered_df[COL_DEM_NO] != ""
].copy()

# =====================================================
# STEP 5 — DEM_NO MUST MATCH ALLOWED PATTERN
# Allowed chars: A-Z, 0-9, /, -
# =====================================================
filtered_df = filtered_df[
    filtered_df[COL_DEM_NO].str.match(r'^[A-Za-z0-9/-]+$')
].copy()

# =====================================================
# MASTER-ID MAPPING
# =====================================================
multi_master_counts = master_df.groupby("Ledger_code")["master_id"].nunique()
multi_master_ledger = multi_master_counts[multi_master_counts > 1].index.tolist()

def get_master_id(row):
    lcode = row[COL_L_CODE]
    ecode = row[COL_E_CODE]

    matches = master_df[master_df["Ledger_code"] == lcode]
    if matches.empty:
        return None, None

    if len(matches) == 1:
        m = matches.iloc[0]
        return m["master_id"], m["eqpt_code"]

    refined = matches[matches["eqpt_code"] == ecode]
    if len(refined) == 1:
        m = refined.iloc[0]
        return m["master_id"], m["eqpt_code"]

    return None, None

master_ids = []
new_eqpt_codes = []
unresolved = 0

for _, row in filtered_df.iterrows():
    mid, new_code = get_master_id(row)
    master_ids.append(mid)
    new_eqpt_codes.append(new_code)

    if mid is None:
        unresolved += 1

original_e_codes = filtered_df[COL_E_CODE].copy()

filtered_df["master_id"] = master_ids
filtered_df["E_CODE"] = new_eqpt_codes

# =====================================================
# SAVE UNRESOLVED MASTER-ID ROWS
# =====================================================
removed_step4_df = filtered_df[filtered_df["master_id"].isna()].copy()
removed_step4_df.to_csv(REMOVED_STEP4_FILE, index=False)

filtered_df = filtered_df[filtered_df["master_id"].notna()]

# =====================================================
# COUNT E_CODE OVERWRITTEN
# =====================================================
overwritten_count = (original_e_codes != filtered_df["E_CODE"]).sum()

# =====================================================
# MOVE master_id TO FRONT
# =====================================================
cols = filtered_df.columns.tolist()
cols.remove("master_id")
filtered_df = filtered_df[["master_id"] + cols]

# =====================================================
# SAVE FINAL OUTPUT
# =====================================================
filtered_df.to_csv(OUTPUT_FILE, index=False)

print("✔ Output saved to:", OUTPUT_FILE)
print("✔ Removed due to master_id unresolved:", len(removed_step4_df))
print("✔ Overwritten E_CODE count:", overwritten_count)
print("✔ Final exported rows:", len(filtered_df))
