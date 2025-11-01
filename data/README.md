# Project Directory Structure and Alembic Usage Guide

This document provides an overview of the directory structure and explains how to manage database schema migrations using Alembic.

---

## Directory Structure

```
data/
│
├── alembic/                     # Alembic migration environment
│   ├── versions/                # Migration scripts that track schema changes
│   │   └── 9584caadb170_create_account_table.py  # Example migration script
│   ├── env.py                   # Alembic environment configuration (modify only if integrating with models)
│   ├── README                   # Alembic-related documentation
│   └── script.py.mako           # Alembic internal template (do not modify)
│
├── models.py                    # Python ORM models defining database schema
├── .env                        # Environment variables (database credentials, not committed)
├── .gitignore                  # Files to be ignored by git
├── Makefile                    # Utility commands to manage PostgreSQL service
├── README.md                   # This documentation file
├── alembic.ini                 # Alembic configuration file (do not modify)
└── docker-compose.yml          # Docker Compose configuration for PostgreSQL (do not modify)
```

---

## Overview

- **`models.py`**: Contains Python classes representing database tables and relationships.
- **`alembic/versions/`**: Contains migration scripts generated to modify database schema.
- **`.env`**: Stores database credentials and other environment variables; keep this file secure.
- Files like `alembic.ini` and `docker-compose.yml` are config files and should not be edited unless necessary.

---

## Common Alembic Commands

Run these commands from the directory containing `alembic.ini`:

### 1. Generate a new migration script after modifying models

```
alembic revision --autogenerate -m "describe your change"
```

This compares your current models in `models.py` with the database schema and creates a migration script in `alembic/versions/`.

---

### 2. Apply migrations to update your database schema

```
alembic upgrade head
```

This runs all pending migrations in order, updating your database to the latest schema.

---

### 3. Rollback (downgrade) the last migration

```
alembic downgrade -1
```

This reverts the most recent schema change.

---

### 4. Start database
```
make dbstart
```
Start the postgres Database

---

### 5. Stop Database

```
make dbstop
```
Stop the postgres Database

---

### Notes:

- Always define or update your database structure in `models.py`.
- Use Alembic commands to keep your database in sync with your models.
- Commit migration scripts in `alembic/versions/` to version control along with your code.
- Use the `Makefile` to start/stop the PostgreSQL database conveniently.
