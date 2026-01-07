import asyncio
import os
import pandas as pd
import logging
from sqlalchemy import insert
from data.models.depot_demand import Dmd_junction
from data.database import get_db, init_db

# Configuration
CSV_DIRECTORY = "apd_processed"
LOG_FILE = "migration_errors.log"

# Setup Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)

def clean_int(value, default=None):
    """Safely convert mixed CSV data to Python Int."""
    if pd.isna(value) or value == '':
        return default
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default

def clean_str(value, max_len=None):
    """
    Safely ensure value is a clean string.
    Preserves leading zeros (e.g., '001' stays '001').
    """
    if pd.isna(value) or value == '':
        return None
    
    # Convert to string and strip whitespace
    s = str(value).strip()
    
    # Handle the ".0" issue if pandas read "001" as float "1.0"
    if s.endswith('.0'):
        try:
            # If it looks like a float ending in .0, try to convert back to int then string
            # This is risky if you have "001.0", so usually direct string is better.
            # But standard pandas read often makes integers floats.
            # If your CSV explicitly has "001", this simple return is best:
            return s
        except:
            pass
            
    # Truncate if max_len is provided
    if max_len and len(s) > max_len:
        return s[:max_len]
        
    return s

async def process_all_files():
    print(f"🚀 Starting Batch Migration from: {CSV_DIRECTORY}")
    print(f"📝 Errors will be saved to: {LOG_FILE}\n")
    
    if not os.path.exists(CSV_DIRECTORY):
        print(f"❌ Directory not found: {CSV_DIRECTORY}")
        return

    all_files = [f for f in os.listdir(CSV_DIRECTORY) if f.endswith('.csv')]
    
    if not all_files:
        print("⚠ No CSV files found.")
        return

    success_count = 0
    fail_count = 0

    async for session in get_db():
        for idx, filename in enumerate(all_files, 1):
            file_path = os.path.join(CSV_DIRECTORY, filename)
            print(f"\rProcessing {idx}/{len(all_files)}: {filename}...", end="", flush=True)

            try:
                # dtype=object is CRITICAL here to preserve '001' as string
                df = pd.read_csv(file_path, dtype=object)
                
                if df.empty:
                    logging.error(f"{filename}: File is empty")
                    fail_count += 1
                    continue

                batch_data = []

                for index, row in df.iterrows():
                    entry = {
                        # --- IDs (Usually purely numeric, keep as Int) ---
                        "Page_id": clean_int(row.get('Page_id')),
                        "dmd_id": clean_int(row.get('dmd_id')),

                        # --- CHANGED TO STRING (Preserves '001', '01') ---
                        # Max length set to 20 to be safe, adjust as needed
                        "demand_no": clean_str(row.get('demand_no'), max_len=20), 
                        "sub_dem_no": clean_str(row.get('SDEM_NO'), max_len=20),
                        "iil_srl": clean_str(row.get('IIL_SRL'), max_len=20),
                        "civil_srl": clean_str(row.get('CVIL_SRL'), max_len=20),

                        # --- Existing Strings ---
                        "Scale_no": clean_str(row.get('SCL_NO'), max_len=30),
                        "Part_no": clean_str(row.get('PART_NO'), max_len=30),
                        "Nomenclature": clean_str(row.get('NOMEN'), max_len=30),
                        "A_u": clean_str(row.get('A_U'), max_len=10),
                        "Dept_ctrl": clean_str(row.get('DEP_CTRL'), max_len=30),
                        
                        # --- Quantities/Math (Must remain Int) ---
                        "Auth": clean_int(row.get('SCL_AUTH')),
                        "Curr_stk_bal": clean_int(row.get('P_STOCK')),
                        "Dues_in": clean_int(row.get('D_IN')),
                        "Outs_Reqd": clean_int(row.get('O_REQD')),
                        "stk_N_yr": clean_int(row.get('STOCK'), default=0),
                        "Reqd_as_OHS": clean_int(row.get('N_REQD'), default=0),
                        "Cons_qty": clean_int(row.get('CONS_QTY'), default=0),
                        "Cons_eqpt": clean_int(row.get('CONS_EQPT')),
                        "Reqd_as_cons": clean_int(row.get('N_REQDCONS'), default=0),
                        "qty_dem": clean_int(row.get('D_QTY'), default=0),
                        "Recd": clean_int(row.get('RCD1'), default=0),
                    }
                    batch_data.append(entry)

                if batch_data:
                    chunk_size = 1000
                    for i in range(0, len(batch_data), chunk_size):
                        chunk = batch_data[i:i + chunk_size]
                        stmt = insert(Dmd_junction).values(chunk)
                        await session.execute(stmt)
                    
                    await session.commit()
                    success_count += 1
                else:
                    logging.error(f"{filename}: No valid data rows found after processing")
                    fail_count += 1

            except Exception as e:
                await session.rollback()
                fail_count += 1
                error_msg = f"{filename}: {str(e)}"
                logging.error(error_msg)

    print(f"\n\n🏁 Migration Finished!")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    
    if fail_count > 0:
        print(f"👉 CHECK '{LOG_FILE}' TO SEE THE ERRORS.")

async def main():
    await init_db()
    await process_all_files()

if __name__ == "__main__":
    asyncio.run(main())