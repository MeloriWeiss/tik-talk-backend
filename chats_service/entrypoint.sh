#!/bin/bash

sed -i 's/\r$//' "$0"

set -x

service_prefix="chats_service"

if [ ! -f /app/.initialized ]; then
  echo "[$service_prefix] First launch, performing migrations and sidings..."

  alembic upgrade head

  python app/seed.py

  touch /app/.initialized
else
  echo "[$service_prefix] Migrations and sidings have already been completed"
fi

exec "$@"