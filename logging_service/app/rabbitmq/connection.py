import asyncio
from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI

from .handle_message import handle_message


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = None
    channel = None
    queue = None

    try:
        connection = await aio_pika.connect_robust("amqp://nazarov:nazarov@rabbitmq:5672/")
        channel = await connection.channel()
        logging_queue = await channel.declare_queue("logging_queue", durable=True)

        def handle_message_sync(msg):
            asyncio.create_task(handle_message(app, msg))

        await logging_queue.consume(handle_message_sync)

        print("[logging_service] Connected and listening to the queue", flush=True)
    except Exception as e:
        print("[logging_service] Error connecting to RabbitMQ:", e, flush=True)

    if connection:
        app.state.rabbit_connection = connection
        app.state.rabbit_channel = channel
        app.state.rabbit_queue = queue
    else:
        app.state.rabbit_connection = None
        app.state.rabbit_channel = None
        app.state.rabbit_queue = None

    yield

    if connection:
        await connection.close()
