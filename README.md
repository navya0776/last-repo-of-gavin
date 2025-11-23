# Data Migration Guide

**CSV → PostgreSQL (Docker)**

This document explains how to migrate CSV-based data into the project’s PostgreSQL database running inside Docker. Follow each step precisely to ensure correct and repeatable migrations.

---

## Table of Contents

1. [Repository Preparation](#1-repository-preparation)
2. [Build Setup](#2-build-setup)
3. [Migration File Placement](#3-migration-file-placement)
4. [Script Responsibilities](#4-script-responsibilities)
5. [Environment Files](#5-environment-files)
6. [Migration Execution Flow](#6-migration-execution-flow)
7. [Windows Notes](#7-windows-specific-notes)

---

## 1. Repository Preparation

1. Ensure your local repository is up to date with the **migration branch**.
2. Stash any uncommitted changes:

   ```bash
   git stash
   ```
3. Switch to the `main` branch and pull upstream changes:

   ```bash
   git checkout main
   git pull upstream main
   ```
4. **Do not rebase** at this stage. The migration code is not fully tested yet.

---

## 2. Build Setup

1. Run a full clean:

   ```bash
   make clean
   ```
2. Ensure all required files are created or updated **before running `make`**.
   If you change files afterward, they won’t appear inside Docker unless you rebuild:

   ```bash
   make clean
   make
   ```
3. Build:

   ```bash
   make
   ```

---

## 3. Migration File Placement

Your project directory must look like this:

```
../
./
.git/
.github/
backend/
csv/
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
issues.txt
pyproject.toml
pytest.ini
```

Place the migration scripts inside `scripts/`:

```
scripts/
  File_creation_1.py
  File_creation_2.py
  ledger_migration.py
  migration_master_tbl.py
  store_migrations.sql
```

---

## 4. Script Responsibilities

### `File_creation_1.py`

* Loads `mastereqpt.csv`
* Adds required new row(s)
* Generates `mastereqpt_processed.csv`

### `File_creation_2.py`

* Uses `mastereqpt_processed.csv`
* Creates a new folder for generated ledger data
* Produces ledger rows containing `store_id` + `ledger_id`

### Conditions

* If the provided data **already includes**:

  * `ledgers/` folder
  * `mastereqpt.csv`
    you may skip `File_creation_1.py` and run only the later steps.

* For a **fresh database**, always start with `File_creation_1.py`.

* All generated folders/files must exist **before running `make`** so they are included in Docker.

---

## 5. Environment Files

Create the following in the repository root.

### `.env_backend`

```
#backend_env
DATABASE_URL=postgresql+psycopg://admin:pass@postgres:5432/ims
REDIS_URL=redis://redis:6379/0
ENV=production
```

### `.env_local`

```
DATABASE_URL=postgresql+psycopg://admin:pass@localhost:5432/ims
```

### `.env_db`

```
#postgres_env
POSTGRES_USER=admin
POSTGRES_PASSWORD=pass
POSTGRES_DB=ims
```

---

## 6. Migration Execution Flow

Run these steps in order:

1. Build containers:

   ```bash
   make
   ```

2. Enter data directory:

   ```bash
   cd data
   ```

3. Apply Alembic migrations:

   ```bash
   make
   ```

   Before running this, **delete all existing Alembic version files**:

   ```
   data/alembic/versions/*.py
   ```

4. Open the backend container:

   ```bash
   make login_app
   ```

5. Run master table migration:

   ```bash
   python -m scripts.migration_master_tbl
   ```

6. Open the DB container:

   ```bash
   make login_db
   ```

7. Execute store migration SQL:

   * Paste content from `scripts/store_migrations.sql`

8. Login to app again:

   ```bash
   make login_app
   ```

9. Run ledger migration:

   ```bash
   python -m scripts.ledger_migration
   ```

---

## 7. Windows-Specific Notes

If migrations fail due to database connection issues on Windows, you may have **two PostgreSQL instances** running:

* Local PostgreSQL service
* Docker PostgreSQL container

Disable the local PostgreSQL service and allow Docker’s instance to run exclusively.

