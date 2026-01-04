# **Data Migration Guide**

**CSV → PostgreSQL (Docker Automated Migration)**

This document explains how CSV-based data is migrated into the project's PostgreSQL database using Docker. The migration process is now fully automated and runs inside the backend container via the entrypoint script.

---

## **Table of Contents**

1. [Repository Preparation](#1-repository-preparation)
2. [Build Setup](#2-build-setup)
3. [Migration File Placement](#3-migration-file-placement)
4. [Script Responsibilities](#4-script-responsibilities)
5. [Environment Files](#5-environment-files)
6. [Automated Migration Flow](#6-automated-migration-flow)
7. [Windows Notes](#7-windows-notes)

---

## **1. Repository Preparation**

1. Ensure your local repository is up to date with the migration branch.
2. Stash any uncommitted changes:

   ```bash
   git stash
   ```
3. Switch to `main` and pull the latest changes:

   ```bash
   git checkout main
   git pull upstream main
   ```
4. Do **not** rebase at this stage.

---

## **2. Build Setup**

Docker packages files at build time. Any changes made *after* building will not appear inside the container.

1. Clean:

   ```bash
   make clean
   ```
2. Ensure all necessary CSV files and generated folders exist *before building*.
3. Build:

   ```bash
   make
   ```

---

## **3. Migration File Placement**

Your repo must follow this structure:

```
.git/
.github/
backend/
data/
dist/
docs/
frontend/
frontend_SAPEAA/
migrations/
scripts/
test/
.env_backend
.env_db
.env_local
.gitignore
.pre-commit-config.yaml
Dockerfile
LICENSE
Makefile
README.md
docker-compose.yml
pyproject.toml
pytest.ini
```

Migration-related scripts live inside:

```
scripts/
  File_creation_1.py
  File_creation_2.py
  migration_master_tbl.py
  store_migration.py
  ledger_migration.py
  entrypoint.sh
```

---

## **4. Script Responsibilities**

### **File_creation_1.py**

* Reads `mastereqpt.csv`
* Adds required new rows
* Outputs `mastereqpt_processed.csv`

### **File_creation_2.py**

* Reads `mastereqpt_processed.csv`
* Creates `ledgers/` output directory
* Generates ledger entries with `store_id` + `ledger_id`

### **migration_master_tbl.py**

* Imports master table records into PostgreSQL

### **insert_stores.py**

*(Replaces old `store_migrations.sql`)*

* Inserts predefined Store rows via async SQLAlchemy

### **ledger_migration.py**

* Loads ledger data into the database

---

## **5. Environment Files**

Create these in your repo root:

### `.env_backend`

```
DATABASE_URL=postgresql+psycopg://admin:pass@db:5432/ims
REDIS_URL=redis://redis:6379/0
ENV=production
```

### `.env_local`

```
DATABASE_URL=postgresql+psycopg://admin:pass@localhost:5432/ims
```

### `.env_db`

```
POSTGRES_USER=admin
POSTGRES_PASSWORD=pass
POSTGRES_DB=ims
```

---

## **6. Automated Migration Flow**

All migrations are now executed **automatically** by the backend container during startup.

### **Execution Order**

1. File_creation_1.py
2. File_creation_2.py
3. migration_master_tbl.py
4. store_migration.py
5. ledger_migration.py
6. Backend server starts automatically

### **Start Everything**

```
make
```

### **Run migration-only mode**

Runs only:

* migration_master_tbl.py
* ledger_migration.py

Command:

```
make migrate_only
```

---

## **7. Windows Notes**

If PostgreSQL fails to connect, ensure you are not running two database instances:

* Local PostgreSQL service
* Docker PostgreSQL container

Disable the local Windows PostgreSQL service and retry.
