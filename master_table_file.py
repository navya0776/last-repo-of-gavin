import csv
import os
import asyncio
import sys

# Same constant as before
HEAD_FIELD = "eqpt_name"


def safe_str(value):
    return value.strip() if value not in (None, "", "NULL") else None


async def convert_csv(input_csv_path: str, output_csv_path: str):
    # Read input CSV
    with open(input_csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        processed_rows = []
        master_id_counter = 1  # auto increment starts from 1

        for row in reader:
            new_row = {
                "master_id": master_id_counter,
                "Ledger_code": safe_str(row.get("L_CODE")),
                "eqpt_code": safe_str(row.get("E_CODE")),
                "ledger_name": safe_str(row.get("L_NAME")),
                HEAD_FIELD: safe_str(row.get("E_NAME"))
            }

            processed_rows.append(new_row)
            master_id_counter += 1

    # Write to NEW CSV file
    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["master_id", "Ledger_code", "eqpt_code", "ledger_name", HEAD_FIELD]
        )
        writer.writeheader()
        writer.writerows(processed_rows)

    print(f"✅ Created new CSV file with {len(processed_rows)} records:")
    print(f"📄 {output_csv_path}")


async def main():
    INPUT_CSV = os.path.join(
        os.path.dirname(__file__),
        "csv/scripts/msteqpt.csv"
    )

    OUTPUT_CSV = os.path.join(
        os.path.dirname(__file__),
        "csv/msteqpt_processed.csv"
    )

    await convert_csv(INPUT_CSV, OUTPUT_CSV)


asyncio.run(main())
