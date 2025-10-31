## Quick context for AI coding agents

- Project layout: Python FastAPI backend in `backend/`; database & migrations in `data/`; tests under `test/`.
- The backend is async (FastAPI + Motor). Key files:
  - `backend/main.py` — application entry; uses an async lifespan to init Redis and Mongo.
  - `data/database/mongo.py` — `MongoManager` initializes `AsyncIOMotorClient` and collections (names use CamelCase like `Store_Ledgers`).
  - `data/run_migrations.py` — migration runner (async); runs `upgrade(db[, session])` functions from `data/migrations`.
  - `backend/services/ledger_crud.py` — example service layer: async methods, HTTPException wrapping, `serialize_doc` pattern for ObjectId -> str.
  - `backend/routers/ledger/routes.py` — routing layer imports services (follow this pattern for new endpoints).

## Architecture & conventions (short)
- Single backend codebase: `backend` package is packaged via `pyproject.toml` (setuptools find: where=["backend"]).
- Async-first design: use `async def`, Motor for Mongo, and `await` for DB calls.
- Database collections are initialized by `MongoManager().init_client()` and used via attributes (e.g. `mongo_manager.store_ledgers`). Always ensure the client is initialized before collection ops.
- Services return serializable dicts (use `serialize_doc` to convert ObjectId). Services raise FastAPI `HTTPException` for HTTP-friendly errors.

## Local developer workflows (explicit commands)
- Install dev/test deps: `pip install -e ".[test]"` from repository root (this sets up test deps and pre-commit hooks).
- Start dev DBs: `docker-compose up -d` (uses `docker-compose.yml` to run `mongo` and `redis`).
- Run migrations: from repo root run `python data/run_migrations.py` (script uses asyncio and will apply unapplied migrations).
- Run app locally: from repo root run `uvicorn backend.main:app --reload` (ensures package imports resolve correctly).
- Run tests: `pytest` (pytest config uses `test/backend_tests` and `test/data_tests`).

## Patterns to follow when editing/adding code
- Router → Service → DB pattern: keep business logic in `backend/services/*` and minimal orchestration in `backend/routers/*`.
- Reuse `MongoManager` for DB access. Avoid creating ad-hoc motor clients across files; call `await MongoManager().init_client()` during setup/lifespan.
- Use the existing `serialize_doc` approach when returning DB documents (convert `_id` and ledger sub-ids to strings).
- For migrations, implement `async def upgrade(db, session=None)` in `data/migrations/*.py` and let `data/run_migrations.py` apply them.
- Tests are async-friendly; prefer `pytest-asyncio` style tests already used in `test/`.

## CI and packaging notes
- CI workflows live in `.github/workflows/` (PR CI uses `pr-ci-backend.yml` which delegates to `backend-action.yml`); keep tests and pyproject changes in scope of those workflows.
- Packaging: `pyproject.toml` defines `ims-backend` and optional extras `test` and `deploy`. Use `python -m build` and `pip install dist/*.whl` only for packaging tasks.

## Examples (copyable patterns)
- Init DB in lifespan (see `backend/main.py`):
  - `redis, client = await asyncio.gather(init_redis(), MongoManager().init_client())`
- Safe insert with serialization (see `backend/services/ledger_crud.py`):
  - Validate inputs, call collection methods (`insert_one`, `find_one`, `aggregate`), then run `serialize_doc` before returning.

## When in doubt
- Search for the pattern you want to match: `ledger_crud.py` (service style), `backend/routers/*` (router shape), and `data/database/mongo.py` (DB lifecycle).
- Prefer minimal, non-breaking changes: keep async signatures, return JSON-serializable types, and raise `HTTPException` for user-visible errors.

---
If anything here is unclear or you'd like more examples (tests, a new router+service scaffold), tell me which area and I will expand this file accordingly.
