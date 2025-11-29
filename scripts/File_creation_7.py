import os
import csv
from collections import defaultdict

#This is the file that is used add the master id with the files that have been converted using the File_creation_7.py and only add those ledger which are present in master_tbl rather than all the ledgers 
# ---------------- USER CONFIG ----------------
MASTER_FILE = "migrations/msteqpt_processed.csv"   # reference file with L_CODE -> master_id
LEDGER_FOLDER = "migrations/provision"            # folder containing ledger CSVs
OUTPUT_FOLDER = "migrations/cds_provision"               # output folder

REF_LCODE_COL = "Ledger_code"         # column in reference file for code
REF_MASTER_ID_COL = "master_id"  # column containing master ID

CDS_LCODE_COL = "L_CODE"      # ledger column to detect L_CODE

PREPEND_MASTER_COLUMN = True     # master_id goes in front; else at end
# ---------------------------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def load_reference(master_path):
    """Load L_CODE -> [master_id,...] mapping."""
    mapping = defaultdict(list)

    with open(master_path, newline="") as f:
        reader = csv.DictReader(f)
        header_map = {h.strip().lower(): h for h in reader.fieldnames}

        ref_code_col = header_map.get(REF_LCODE_COL.lower())
        ref_mid_col = header_map.get(REF_MASTER_ID_COL.lower())

        if ref_code_col is None or ref_mid_col is None:
            raise ValueError(
                f"Columns '{REF_LCODE_COL}' and '{REF_MASTER_ID_COL}' must exist in reference file."
            )

        for row in reader:
            code = (row.get(ref_code_col, "") or "").strip().upper()
            mid = (row.get(ref_mid_col, "") or "").strip()
            if code and mid:
                mapping[code].append(mid)

    return mapping


def find_column_index(header, target):
    """Case-insensitive column match."""
    target = target.lower()
    for i, col in enumerate(header):
        if col.lower() == target:
            return i
    return None


def process_ledgers(mapping):
    for fname in sorted(os.listdir(LEDGER_FOLDER)):
        if not fname.lower().endswith(".csv"):
            continue

        in_path = os.path.join(LEDGER_FOLDER, fname)

        with open(in_path, newline="") as f:
            reader = csv.reader(f)

            try:
                header = next(reader)
            except StopIteration:
                continue  # empty file, ignore

            # detect L_CODE column index
            lcode_idx = find_column_index(header, CDS_LCODE_COL)
            if lcode_idx is None:
                continue  # skip files without L_CODE column entirely

            # read FIRST data row to get the ledger’s L_CODE
            first_row = None
            for r in reader:
                if len(r) == 0 or all(x.strip() == "" for x in r):
                    continue
                first_row = r
                break

            if first_row is None:
                continue  # no rows, skip file

            file_code = (first_row[lcode_idx] or "").strip().upper()
            master_ids = mapping.get(file_code, [])

            # -------- SKIP output files with no matching L_CODE --------
            if not master_ids:
                continue

            # Re-read entire ledger from start since we consumed rows
            with open(in_path, newline="") as lf, \
                 open(os.path.join(OUTPUT_FOLDER, fname), "w", newline="") as of:

                reader2 = csv.reader(lf)
                writer = csv.writer(of)

                next(reader2, None)  # skip header again

                master_col = REF_MASTER_ID_COL
                if PREPEND_MASTER_COLUMN:
                    new_header = [master_col] + header
                else:
                    new_header = header + [master_col]

                writer.writerow(new_header)

                for row in reader2:
                    # duplicate full ledger rows for each master_id
                    for mid in master_ids:
                        if PREPEND_MASTER_COLUMN:
                            writer.writerow([mid] + row)
                        else:
                            writer.writerow(row + [mid])


def main():
    mapping = load_reference(MASTER_FILE)
    process_ledgers(mapping)
    print("Done.")


if __name__ == "__main__":
    main()
