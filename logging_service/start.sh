#!/bin/bash

host="${RABBITMQ_HOST:-tik-talk-rabbitmq-1}"
port="${RABBITMQ_PORT:-5672}"
max_attempts=20
attempt=1
timeout=5
service_prefix="logging_service"

echo "[$service_prefix] Waiting for RabbitMQ at $host:$port..."
while ! nc -z -w "$timeout" "$host" "$port"; do
  if [ "$attempt" -ge "$max_attempts" ]; then
    echo "[$service_prefix] RabbitMQ is not available after $attempt attempts. Exiting."
    exit 1
  fi
  echo "[$service_prefix] Attempt $attempt/$max_attempts failed. Retrying in $timeout seconds..."
  attempt=$((attempt + 1))
  sleep "$timeout"
done

echo "[$service_prefix] RabbitMQ is available! Starting application..."
exec "$@"