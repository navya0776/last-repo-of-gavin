all:
	@echo "Building docker containers backend"
	@docker compose up -d --build

logs:
	@echo "Showing docker compose logs"
	@docker compose logs -f backend

ledger:
	@echo "Sending ledger to database"
	python -m scripts/ledger_migration.py

mastertbl:
	@echo "Sending mastertbl to database"
	python -m scripts/migration_master_tbl.py

clean:
	@echo "Stopping and removing docker containers"
	@docker compose down -v
	@rm -rf data/alembic/versions/*.py




