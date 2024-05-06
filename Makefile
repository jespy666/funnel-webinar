REVISION_CMD = alembic revision --autogenerate -m

.PHONY: migrations run

migrations:
	$(REVISION_CMD) "$(shell read -p 'Введите название миграции: ' msg; echo $$msg)"

migrate:
	alembic upgrade head

run:
	python3 ./src/app.py