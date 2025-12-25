import json

import aio_pika
from fastapi import FastAPI

from .handlers.handle_http_log import handle_http_log
from .utils.send_response import send_response


async def handle_message(app: FastAPI, message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        print("[logging service] Message received:", body, flush=True)

        data = json.loads(body)
        message_log_type = data.get("log_type")
        message_data = data.get("data")

        response = None

        if message_log_type == "http":
            response = await handle_http_log(message_data)

        await send_response(app.state.rabbit_channel, response, message.reply_to, message.correlation_id)
