login:
	@docker compose exec db psql -U admin -d ims

alembic-auto:
	@alembic revision --autogenerate -m "$(m)"

alembic-upgrade:alembic-auto
	@alembic upgrade head
