# Project Directory Structure and MongoDB Migration Guide

This document describes the backend data directory structure and explains how to manage **MongoDB schema and data migrations** using the custom migration runner (`run_migrations.py`).

---

## 📁 Directory Structure

```
data/
│
├── migrations/                     # Migration scripts (Python files) applied in order
│   ├── __pycache__/                # Python bytecode cache (ignore)
│   └── 001_create_users_collection.py  # Example migration script
│
├── run_migrations.py               # Migration runner (applies migrations to MongoDB)
│
├── .env                            # Environment variables (MongoDB connection string, not committed)
├── .gitignore                      # Files ignored by git
├── Makefile                        # Utility commands to start/stop MongoDB service via Docker
├── README.md                       # This documentation file
└── docker-compose.yml              # Docker Compose configuration for MongoDB
```

---

## ⚙️ Overview

* **`migrations/`**
  Contains numbered Python scripts defining database changes (e.g. creating collections, indexes, seeding data).
  Each file defines:

  ```python
  def upgrade(db, session=None):
      # Apply this migration

  def downgrade(db, session=None):
      # Revert this migration
  ```

* **`run_migrations.py`**
  Orchestrates migrations:

  * Connects to MongoDB using the URI from `.env` (`DATABASE_URL`).
  * Tracks applied migrations in a `migrations` collection.
  * Runs new migration scripts in ascending order.
  * Supports transactions when running on a **replica set**.

* **`.env`**
  Stores environment variables such as the MongoDB URI. Example:

  ```
  DATABASE_URL=mongodb://ims_root:ims_root_pw@localhost:27017/ims?authSource=admin
  ```

* **`docker-compose.yml`**
  Defines a local MongoDB container environment for development and testing.

* **`Makefile`**
  Provides short commands to control the MongoDB service.

---

## 🧩 Common Commands

All commands are run from the `data/` directory.

### 1. Run migrations

Apply all pending migrations in order:

```bash
python run_migrations.py
```

This connects to MongoDB and applies any new scripts found in `data/migrations/`.

---

### 2. Create a new migration file

Create a new migration under `data/migrations/` with the next sequential number:

```bash
touch data/migrations/002_add_roles_index.py
```

Example content:

```python
from pymongo import ASCENDING

def upgrade(db, session=None):
    db.users.create_index([("role", ASCENDING)], name="role_idx")

def downgrade(db, session=None):
    db.users.drop_index("role_idx")
```

---

### 3. View applied migrations

Run a quick check in MongoDB:

```bash
mongosh ims --eval "db.migrations.find().pretty()"
```

Each document represents a migration applied by `run_migrations.py`.

---

### 4. Start MongoDB (Docker)

```bash
make dbstart
```

Starts MongoDB using `docker-compose`.

---

### 5. Stop MongoDB

```bash
make dbstop
```

Stops the MongoDB container.

---

## 🧠 Notes

* Define your database collections and indexes inside migration scripts, not manually in the DB.
* `run_migrations.py` ensures every migration runs only once.
* Migration filenames must start with a zero-padded number (e.g., `001_`, `002_`) for ordering.
* For replica set support (transactions), ensure MongoDB is started with `--replSet` and initialized with `rs.initiate()`.
* Do **not** modify or delete already applied migration files — instead, create a new one to change schema or data.
* Keep `.env` and credentials secure.

---

## ✅ Example Migration History

After running two migrations, your database `ims` will contain:

```
migrations/
 ├── 001_create_users_collection.py
 └── 002_add_roles_index.py
```

and the MongoDB `migrations` collection will show:

```json
[
  { "name": "001_create_users_collection.py", "applied_at": "2025-10-17T21:00:00Z" },
  { "name": "002_add_roles_index.py", "applied_at": "2025-10-17T21:05:00Z" }
]
```
