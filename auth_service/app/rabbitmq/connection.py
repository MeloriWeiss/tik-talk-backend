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
        auth_queue = await channel.declare_queue("auth_service_queue", durable=True)
        # chats_queue = await channel.declare_queue("chats_service_queue", durable=True)

        def handle_message_sync(msg):
            asyncio.create_task(handle_message(app, msg))

        await auth_queue.consume(handle_message_sync)
        # await chats_queue.consume(handle_message_sync)
        print("Подключено и слушаем очередь", flush=True)
    except Exception as e:
        print("Ошибка подключения к RabbitMQ:", e, flush=True)

    if connection:
        app.state.rabbit_connection = connection
        app.state.rabbit_channel = channel
        app.state.rabbit_queue = queue
        # app.state.rabbit_queue = {
        #     "auth_service_queue": auth_service_queue,
        #     "chats_service_queue": chats_service_queue
        # }
    else:
        app.state.rabbit_connection = None
        app.state.rabbit_channel = None
        app.state.rabbit_queue = None

    yield

    # Закрываем соединение, если оно есть
    if connection:
        await connection.close()
