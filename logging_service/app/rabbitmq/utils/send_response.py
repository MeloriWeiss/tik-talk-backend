import json
import aio_pika


async def send_response(channel, response_data, reply_to, correlation_id):
    if channel and reply_to:
        message_body = json.dumps(response_data).encode()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body,
                correlation_id=correlation_id,
            ),
            routing_key=reply_to
        )
