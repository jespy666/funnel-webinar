.PHONY: migrations

migrations:
    alembic revision --autogenerate -m "$(name)"

migrate:
    alembic upgrade head