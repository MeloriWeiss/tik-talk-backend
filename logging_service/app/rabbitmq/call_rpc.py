import asyncio
import json
import uuid

import aio_pika

async def call_rpc(service_queue: str, message: dict, timeout=5):
    connection = await aio_pika.connect_robust("amqp://nazarov:nazarov@rabbitmq:5672/")

    async with connection:
        channel = await connection.channel()

        callback_queue = await channel.declare_queue(exclusive=True)

        correlation_id = str(uuid.uuid4())

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                reply_to=callback_queue.name,
                correlation_id=correlation_id,
            ),
            routing_key=service_queue,
        )

        # Ждем ответа
        future = asyncio.Future()

        async def on_response(msg: aio_pika.IncomingMessage):
            if msg.correlation_id == correlation_id:
                future.set_result(msg.body)
                await msg.ack()

        def on_response_sync(msg):
            asyncio.create_task(on_response(msg))

        await callback_queue.consume(on_response_sync)

        try:
            response_body = await asyncio.wait_for(future, timeout)
            return json.loads(response_body.decode())
        except asyncio.TimeoutError:
            return None