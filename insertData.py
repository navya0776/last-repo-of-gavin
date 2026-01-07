import psycopg2

# -------- DATABASE CONFIG -------- #
DB_CONFIG = {
    "host": "localhost",
    "database": "ims",
    "user": "admin",        # or your actual username
    "password": "pass",
    "port": 5432
}


# -------- SQL QUERIES -------- #
TRUNCATE_QUERIES = """
TRUNCATE TABLE
    "demand_junc_ledger",
    "Demand_table",
    "job_ledger",
    "job_master",
    "ledger",
    "master_table",
    "stores",
    "Users"
RESTART IDENTITY CASCADE;
"""

INSERT_QUERIES = """
INSERT INTO "stores" ("store_id", "store_name") VALUES
(1, 'Central Store'),
(2, 'Mechanical Store'),
(3, 'Electrical Store'),
(4, 'Spare Parts Store'),
(5, 'Field Store');

INSERT INTO "master_table" (
    "Master_id", "Ledger_code", "eqpt_code", "ledger_name", "eqpt_name"
) VALUES
(1, 'L001',  'E001', 'LEDGER-01', 'Compressor'),
(2, 'L002',  'E002', 'LEDGER-02', 'Pump'),
(3, 'L003', 'E003', 'LEDGER-03', 'Generator'),
(4, 'L004', 'E004', 'LEDGER-04', 'Transformer'),
(5, 'L005', 'E005', 'LEDGER-05', 'Motor');

INSERT INTO "Users" (
    username,
    password,
    new_user,
    role,
    permissions
)
VALUES (
    'navya',
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    TRUE,
    'admin',
    '{
        "ledger": {"read": true, "write": true},
        "apd": {"read": true, "write": true},
        "overhaul_scale": {"read": true, "write": true},
        "recieve_voucher": {"read": true, "write": true},
        "issue_voucher": {"read": true, "write": true},
         "cds":{"read":true,"write":true},
        "local_purchase_indent": {"read": true, "write": true},
        "local_purchase_quotation": {"read": true, "write": true},
        "local_purchase_recieved": {"read": true, "write": true},
        "local_purchase_ordinance": {"read": true, "write": true},
        "local_purchase_pay": {"read": true, "write": true},
        "local_purchase_query": {"read": true, "write": true},
        "local_purchase_ammend": {"read": true, "write": true}
    }'::json
);

INSERT INTO "ledger" (
    "ledger_id", "store_id", "Master_id", "Ledger_code", "ledger_page",
    "part_number", "nomenclature", "a_u", "stock", "rate",
    "br_stock", "br_stock_dt", "lock_dt", "stock_dt", "yn"
) VALUES
(1, 1, 1, 'L001', 'PG-01', 'P-1001', 'Air Compressor', 'NOS', 50, 1200.50,
 5, '2025-01-01', '2025-01-10', '2025-01-05', 'Y'),
(2, 2, 2, 'L002', 'PG-02', 'P-1002', 'Hydraulic Pump', 'NOS', 30, 950.00,
 3, '2025-01-02', '2025-01-11', '2025-01-06', 'Y'),
(3, 3, 3, 'L003', 'PG-03', 'P-1003', 'Diesel Generator', 'NOS', 10, 55000.00,
 1, '2025-01-03', '2025-01-12', '2025-01-07', 'N'),
(4, 4, 4, 'L004', 'PG-04', 'P-1004', 'Power Transformer', 'NOS', 7, 75000.00,
 1, '2025-01-04', '2025-01-13', '2025-01-08', 'Y'),
(5, 5, 5, 'L005', 'PG-05', 'P-1005', 'Electric Motor', 'NOS', 20, 18000.00,
 2, '2025-01-05', '2025-01-14', '2025-01-09', 'Y');

INSERT INTO "job_master" ("job_id", master_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

INSERT INTO "job_ledger" ("job_id", "ledger_id") VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);


INSERT INTO "Demand_table" (
    "eqpt_id", "master_id", "eqpt_code", "demand_no", "demand_type",
    "eqpt_name", "fin_year", "demand_auth", "full_received",
    "part_received", "outstanding", "percent_received",
    "remarks", "is_locked"
) VALUES
(1, 1, 'E001', 101, 'APD', 'Compressor', '2024-2025',
 'CE Approval', 0, 0, 10, 0.0, 'Initial demand', FALSE),
(2, 2, 'E002', 102, 'SPD', 'Pump', '2024-2025',
 'Store Officer', 5, 0, 5, 50.0, 'Partial received', FALSE),
(3, 3, 'E003', 103, 'APD', 'Generator', '2024-2025',
 'DG Approval', 10, 0, 0, 100.0, 'Fully received', TRUE),
(4, 4, 'E004', 104, 'SPD', 'Transformer', '2024-2025',
 'Division Head', 0, 2, 8, 20.0, 'Pending supply', FALSE),
(5, 5, 'E005', 105, 'APD', 'Motor', '2024-2025',
 'Workshop Auth', 3, 0, 7, 30.0, 'Urgent demand', FALSE);

INSERT INTO "demand_junc_ledger" (
    "Page_id", "dmd_id", "demand_no", "Scale_no", "Part_no",
    "Nomenclature", "A_u", "Auth", "Curr_stk_bal", "Dues_in",
    "Outs_Reqd", "stk_N_yr", "Reqd_as_OHS", "Cons_pattern",
    "qty_dem", "Recd", "Dept_ctrl", "Dept_ctrl_dt"
) VALUES
(1, 1, 101, 'S-01', 'P-1001', 'Compressor', 'NOS',
 10, 50, 5, 10, 2, 1, '5/2', 10, 0, 'MECH', '2025-01-01'),
(2, 2, 102, 'S-02', 'P-1002', 'Pump', 'NOS',
 10, 30, 3, 5, 1, 0, '3/1', 5, 5, 'HYD', '2025-01-02'),
(3, 3, 103, 'S-03', 'P-1003', 'Generator', 'NOS',
 10, 10, 0, 0, 0, 0, '2/0', 10, 10, 'ELEC', '2025-01-03'),
(4, 4, 104, 'S-04', 'P-1004', 'Transforme', 'NOS',
 10, 7, 1, 8, 2, 1, '4/2', 8, 0, 'POWER', '2025-01-04'),
(5, 5, 105, 'S-05', 'P-1005', 'Motor', 'NOS',
 10, 20, 2, 7, 1, 0, '6/3', 7, 3, 'WORKS', '2025-01-05');
"""

# -------- EXECUTION -------- #
def run_queries():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.execute(TRUNCATE_QUERIES)
        cur.execute(INSERT_QUERIES)
        conn.commit()
        print("✅ Tables truncated and data inserted successfully")

    except Exception as e:
        conn.rollback()
        print("❌ Error:", e)

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    run_queries()