import pandas as pd
import os
import re
import logging
import glob
from datetime import datetime

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
INPUT_CSV_FOLDER = r'for_Analysis/processed/valid'
OUTPUT_CSV_FOLDER = r'apd_processed'

DEMAND_INDEX_FILE = r'demand_table_with_indx.csv'
LEDGER_INDEX_FILE = r'ledger_with_indx.csv'

# Column Headers (Internal Name : Actual CSV Header)
COLS_DMD_IDX = {
    'demand_no': 'demand_no',
    'dem_dt': 'dem_dt',
    'eqpt_id': 'eqpt_id',
    'master_id': 'master_id'
}

COLS_LEDGER_IDX = {
    'master_id': 'Master_id',
    'ledger_page': 'ledger_page',
    'ledger_id': 'ledger_id'
}

COLS_DATA_CSV = {
    'l_page': 'L_PAGE',
    'dem_no': 'DEM_NO',
    'dem_dt': 'DEM_DT'
}

# ==========================================
# 📝 LOGGING
# ==========================================
logging.basicConfig(
    filename='migration_process.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)
logger = logging.getLogger()

# ==========================================
# 🛠️ UTILITY FUNCTIONS
# ==========================================

def clean_id(val):
    """
    ULTRA-ROBUST ID CLEANER:
    1. Force to String & Upper Case
    2. Remove whitespace
    3. Remove ANY trailing zeros decimals (.0, .00, .000)
    4. Preserves leading zeros (e.g. '0012' stays '0012')
    """
    if pd.isna(val):
        return ""
    
    # Standardize string
    s = str(val).strip().upper().replace("\r", "").replace("\n", "")
    
    # ⚡ THE FIX: Regex to remove .0, .00, .000 at the end of string
    # Matches a dot, followed by one or more '0's, followed by end of line ($)
    s = re.sub(r'\.0+$', '', s)
    
    return s

def parse_date(date_val):
    """Try multiple formats to return a standard Python date object"""
    if pd.isna(date_val) or date_val == '': return None
    if isinstance(date_val, (datetime, pd.Timestamp)): return date_val.date()
    
    date_str = str(date_val).strip()
    formats = ['%d/%m/%y', '%d-%m-%Y', '%d%m%y', '%Y-%m-%d', '%d/%m/%Y']
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None

def parse_filename_info(filename):
    """Parses '05A040123.csv' -> DemNo: '05A', Date"""
    base_name = os.path.splitext(filename)[0]
    match = re.search(r'(.+)(\d{6})$', base_name)
    
    if match:
        raw_dem = match.group(1)
        raw_date = match.group(2)
        return clean_id(raw_dem), parse_date(raw_date)
    return None, None

# ==========================================
# 🚀 MAIN PROCESSING LOGIC
# ==========================================

def main():
    if not os.path.exists(OUTPUT_CSV_FOLDER):
        os.makedirs(OUTPUT_CSV_FOLDER)
    
    logger.info("=== 🚀 STARTING FINAL MIGRATION (FIXED .00 ISSUE) ===")

    # -----------------------------------------------------------
    # 1. LOAD INDICES (With dtype=str)
    # -----------------------------------------------------------
    try:
        # --- DEMAND INDEX ---
        df_dmd_idx = pd.read_csv(DEMAND_INDEX_FILE, dtype=str)
        
        # Build Lookup Dictionary
        dmd_lookup = {}
        for _, row in df_dmd_idx.iterrows():
            d_no = clean_id(row[COLS_DMD_IDX['demand_no']])
            d_dt = parse_date(row[COLS_DMD_IDX['dem_dt']])
            
            dmd_lookup[(d_no, d_dt)] = {
                'mid': clean_id(row[COLS_DMD_IDX['master_id']]),
                'eid': row[COLS_DMD_IDX['eqpt_id']]
            }
        logger.info(f"✅ Loaded Demand Index")

        # --- LEDGER INDEX ---
        df_led_idx = pd.read_csv(LEDGER_INDEX_FILE, dtype=str)
        
        # Build Lookup Dictionary
        # We clean the page number here so '12.00' becomes '12' in our map
        led_lookup = {}
        for _, row in df_led_idx.iterrows():
            m_id = clean_id(row[COLS_LEDGER_IDX['master_id']])
            # '12.00' -> clean_id -> '12'
            p_no = clean_id(row[COLS_LEDGER_IDX['ledger_page']])
            l_id = row[COLS_LEDGER_IDX['ledger_id']]
            
            led_lookup[(m_id, p_no)] = l_id
            
        logger.info(f"✅ Loaded Ledger Index (Pages normalized)")

    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR LOADING INDICES: {e}")
        return

    # -----------------------------------------------------------
    # 2. PROCESS CSV FILES
    # -----------------------------------------------------------
    csv_files = glob.glob(os.path.join(INPUT_CSV_FOLDER, "*.csv"))
    success_count = 0
    fail_count = 0

    for filepath in csv_files:
        filename = os.path.basename(filepath)
        
        try:
            # Read CSV as string
            df = pd.read_csv(filepath, dtype=str)
            if df.empty: continue

            # --- STEP A: IDENTIFY DEMAND ---
            target_dem, target_dt = parse_filename_info(filename)
            
            # Fallback to content
            if not target_dem and COLS_DATA_CSV['dem_no'] in df.columns:
                target_dem = clean_id(df.iloc[0][COLS_DATA_CSV['dem_no']])
                target_dt = parse_date(df.iloc[0][COLS_DATA_CSV['dem_dt']])

            if not target_dem or not target_dt:
                logger.error(f"❌ {filename}: Could not determine Demand/Date")
                fail_count += 1
                continue

            # --- STEP B: MATCH DEMAND INDEX ---
            dmd_info = dmd_lookup.get((target_dem, target_dt))
            
            if not dmd_info:
                logger.warning(f"⛔ {filename}: No Match for Demand '{target_dem}' / {target_dt}")
                fail_count += 1
                continue

            master_id = dmd_info['mid']
            dmd_id = dmd_info['eid']

            # --- STEP C: ENRICH & MAP LEDGER ---
            df['demand_no'] = target_dem
            df['dmd_id'] = dmd_id
            
            if COLS_DATA_CSV['l_page'] in df.columns:
                # '12' -> clean_id -> '12'
                # Now '12' matches the cleaned '12' from the index
                df['__clean_page'] = df[COLS_DATA_CSV['l_page']].apply(clean_id)
                
                df['Page_id'] = df['__clean_page'].apply(lambda p: led_lookup.get((master_id, p), None))
                
                # Log success rate for this file
                matched = df['Page_id'].notna().sum()
                total = len(df)
                if matched < total:
                    logger.warning(f"⚠️  {filename}: {total - matched}/{total} rows missing Ledger ID.")
                
                df.drop(columns=['__clean_page'], inplace=True)
            else:
                 df['Page_id'] = None

            # --- STEP D: SAVE ---
            # Reorder columns
            cols = df.columns.tolist()
            front = ['Page_id', 'dmd_id', 'demand_no']
            new_order = front + [c for c in cols if c not in front]
            df = df[new_order]
            
            out_path = os.path.join(OUTPUT_CSV_FOLDER, filename)
            df.to_csv(out_path, index=False)
            logger.info(f"✅ Processed: {filename}")
            success_count += 1

        except Exception as e:
            logger.error(f"❌ Error in {filename}: {e}", exc_info=True)
            fail_count += 1

    print(f"Done. Processed {success_count} files. Check logs.")

if __name__ == "__main__":
    main()