import csv
import os

MASTER_FILE = "migrations/msteqpt_processed.csv"        # master converted file
STORE_MAP_FILE = "migrations/msteqpt.csv"
LEDGER_FOLDER = "migrations/raw_ledger"         # folder containing non fmt ledger CSVs
OUTPUT_FOLDER = "migrations/ledgers"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -------------------------------------
# 1️⃣ Load master file → ledger_name → list of master_ids
# -------------------------------------
ledger_master_map = {}

with open(MASTER_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        ledger_name = row["ledger_name"].strip()
        master_id = row["master_id"].strip()

        ledger_master_map.setdefault(ledger_name, []).append(master_id)


# -------------------------------------
# 2️⃣ Load store_id (S_CODE) mapping → L_NAME → store_id
# -------------------------------------
store_map = {}

with open(STORE_MAP_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        ledger_name = row["L_NAME"].strip()
        store_id = row["S_CODE"].strip()
        store_map[ledger_name] = store_id


# -------------------------------------
# 3️⃣ Process each ledger CSV
# -------------------------------------
for ledger_name, master_ids in ledger_master_map.items():

    ledger_file = os.path.join(LEDGER_FOLDER, f"{ledger_name}.csv")

    if not os.path.exists(ledger_file):
        print(f"❌ Missing file: {ledger_file}")
        continue

    print(f"✔ Processing: {ledger_file}")

    store_id = store_map.get(ledger_name, "")

    # Read ledger csv
    with open(ledger_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        ledger_rows = list(reader)

    header = ledger_rows[0]

    # new header (add master_id + store_id at the front)
    new_header = ["master_id", "store_id"] + header
    new_rows = [new_header]

    # Data rows
    for master_id in master_ids:
        for idx, row in enumerate(ledger_rows):
            if idx == 0:
                continue  # skip header

            new_rows.append([master_id, store_id] + row)

    # Save updated CSV
    out_file = os.path.join(OUTPUT_FOLDER, f"{ledger_name}.csv")

    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    print(f"✅ Saved:", out_file)

print("\n🎉 Done! All ledger CSVs updated with master_id + store_id.")
