all:
	@alembic revision --autogenerate -m "$(m)"
	@alembic upgrade head

test:
	curl -X POST http://localhost:8000/auth/login -d '{"username":"admin","password":"admin"}' -H "Content-Type: application/json"

login_db:
	@docker compose exec db psql -U admin -d ims

login_app:
	@docker compose exec backend bash
