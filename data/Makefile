all:
	@alembic revision --autogenerate -m "$(m)"
	@alembic upgrade head

login:
	@docker compose exec db psql -U admin -d ims


