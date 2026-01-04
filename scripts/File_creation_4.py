import pandas as pd

# -----------------------------
# FILE PATHS — CHANGE THESE
# -----------------------------
main_file = "migrations/filtered_job_csvs/filtered_mstjob.csv"               # File where you want MASTER_ID added
mapping_file = "migrations/msteqpt_processed.csv"         # File containing eqpt_code + master_id
output_file = "migrations/jobmaster_with_master_id.csv"

# -----------------------------
# COLUMN NAMES — CHANGE IF NEEDED
# -----------------------------
main_code_col = "E_CODE"             # Column in main file
mapping_code_col = "eqpt_code"       # Column in mapping file
mapping_master_col = "master_id"     # Master ID column in mapping file

# -----------------------------
# LOAD BOTH FILES
# -----------------------------
df_main = pd.read_csv(main_file, dtype=str)
df_map  = pd.read_csv(mapping_file, dtype=str)

# -----------------------------
# MERGE ON E_CODE → eqpt_code
# LEFT JOIN so main file stays same
# -----------------------------
df_merged = df_main.merge(
    df_map[[mapping_code_col, mapping_master_col]],
    how="left",
    left_on=main_code_col,
    right_on=mapping_code_col
)

# -----------------------------
# Insert master_id as FIRST COLUMN
# -----------------------------
# Remove the right-side code column if merge created one
if mapping_code_col in df_merged.columns:
    df_merged.drop(columns=[mapping_code_col], inplace=True)

# Move master_id to front
master_id_col = df_merged.pop(mapping_master_col)
df_merged.insert(0, mapping_master_col.upper(), master_id_col)

first_four_cols = df_merged.columns[:4]
df_merged.dropna(subset=first_four_cols, how="all", inplace=True)

# -----------------------------
# SAVE OUTPUT
# -----------------------------
df_merged.to_csv(output_file, index=False)

print("✔ Done! File saved as:", output_file)
