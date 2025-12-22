#!/bin/bash

service_prefix="main_service"

if [ ! -f /app/.initialized ]; then
    echo "[$service_prefix] First launch, performing migrations and sidings..."

    alembic upgrade head

    python app/seed.py

    touch /app/.initialized
else
    echo "[$service_prefix] Migrations and sidings have already been completed"
fi

exec "$@"