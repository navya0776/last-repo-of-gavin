all: 
	@echo "Building docker containers backend"
	@docker compose up -d --build backend

data:
	@echo "Building docker containers backend"
	@make -C data
	@sleep 2

db:
	@echo "Starting postgres and redis"
	@docker compose up -d db redis
	@sleep 2

logs:
	@echo "Showing docker compose logs"
	@docker compose logs -f backend

clean:
	@echo "Stopping and removing docker containers"
	@docker compose down -v
	@rm -rf data/alembic/versions/*.py




