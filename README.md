## The Mapping is done so that you know what each files tell and means

a. **Migration_master_tbl.py** – Migrates master-table data from `final_csv/msteqpt.csv`.
b. **File_creation_1.py** – Generates an intermediate file used to build a ledger that links `store_id` and `master_id`.
c. **File_creation_2.py** – Produces the `mapped_ledger` folder, where each ledger file is named using the paired `master_id` and `store_id`.

