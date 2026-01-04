# Detect OS and define cross-platform sleep command
ifeq ($(OS),Windows_NT)
    SLEEP = powershell -Command "Start-Sleep -Seconds 2"
    RM = powershell -Command "Remove-Item -Recurse -Force"
else
    SLEEP = sleep 2
    RM = rm -rf
endif

all: data
	@echo "Building docker containers backend"
	@docker compose up -d --build backend

data: db
	@echo "Building docker containers backend"
	@make -C data
	@$(SLEEP)

db:
	@echo "Starting postgres and redis"
	@docker compose up -d db redis
	@$(SLEEP)

logs:
	@echo "Showing docker compose logs"
	@docker compose logs -f backend

clean:
	@echo "Stopping and removing docker containers"
	@docker compose down -v
	@$(RM) data/alembic/versions/*.py




