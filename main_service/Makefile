freeze_deps:
	pip freeze > requirements.txt

init_migrations:
	docker exec -it tik-talk-main_service-1 python -m alembic init app/migrations

create_migration:
	docker exec -it tik-talk-main_service-1 alembic revision --autogenerate -m "Initial migration"

migrate:
	docker exec -it tik-talk-main_service-1 alembic upgrade head

seed:
	docker exec -it tik-talk-main_service-1 python app/seed.py