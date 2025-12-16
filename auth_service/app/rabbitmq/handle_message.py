import json

import aio_pika
from fastapi import FastAPI

from .handlers.handle_login import handle_login
from .handlers.handle_logout import handle_logout
from .handlers.handle_refresh import handle_refresh
from .handlers.handle_register import handle_register
from .handlers.handle_verify_token import handle_verify_token
from .utils.send_response import send_response


async def handle_message(app: FastAPI, message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        print("Получено сообщение:", body, flush=True)

        data = json.loads(body)
        message_action = data.get("action")

        response = None

        if message_action == "verify_token":
            response = await handle_verify_token(data)
        elif message_action == "refresh":
            response = await handle_refresh(data)
        elif message_action == "login":
            response = await handle_login(data)
        elif message_action == "register":
            response = await handle_register(data)
        elif message_action == "logout":
            response = await handle_logout(data)

        await send_response(app.state.rabbit_channel, response, message.reply_to, message.correlation_id)
