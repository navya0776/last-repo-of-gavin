all:
	@echo "Building docker containers backend"
	@docker compose up -d --build

logs:
	@echo "Showing docker compose logs"
	@docker compose logs -f backend

clean:
	@echo "Stopping and removing docker containers"
	@docker compose down -v
	@rm -rf data/alembic/versions/*.py
