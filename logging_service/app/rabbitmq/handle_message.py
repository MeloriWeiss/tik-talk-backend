import json

import aio_pika
from fastapi import FastAPI

from .handlers.handle_log_critical import handle_log_critical
from .handlers.handle_log_error import handle_log_error
from .handlers.handle_log_info import handle_log_info
from .utils.send_response import send_response


async def handle_message(app: FastAPI, message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        print("[logging service] Message received:", body, flush=True)

        data = json.loads(body)
        message_log_level = data.get("log_level")

        response = None

        if message_log_level == "info":
            response = await handle_log_info(data)
        elif message_log_level == "error":
            response = await handle_log_error(data)
        elif message_log_level == "critical":
            response = await handle_log_critical(data)

        await send_response(app.state.rabbit_channel, response, message.reply_to, message.correlation_id)
