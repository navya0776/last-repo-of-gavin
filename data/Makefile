all:
	@alembic revision --autogenerate -m "$(m)"
	@alembic upgrade head

test:
	curl -X POST http://localhost:8000/auth/login -d '{"username":"admin","password":"admin"}' -H "Content-Type: application/json"

login:
	@docker compose exec db psql -U admin -d ims
