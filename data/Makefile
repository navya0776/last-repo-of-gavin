dbstart:
	@echo "Starting mongo databse"
	@docker compose up -d

dbstop:
	@echo "Stopping mongo database"
	@docker compose down -v

mongo_test:
	@echo "Smoke test for mongo"
	@python ../test/data_tests/mongo_test.py

redis_test:
	@echo "Smoke test for redis"
	@python ../test/data_tests/redis_test.py
