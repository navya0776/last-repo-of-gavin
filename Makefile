all:
	@echo "Starting docker containers"
	@docker compose up -d

build:
	@echo "Building docker containers backend"
	@docker compose up -d --build backend

clean:
	@echo "Stopping and removing docker containers"
	@docker compose down -v
