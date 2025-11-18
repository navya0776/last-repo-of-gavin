all:
	@echo "Building docker containers backend"
	@docker compose up -d --build

clean:
	@echo "Stopping and removing docker containers"
	@docker compose down -v
	@rm -rf data/alembic/versions/*.py
