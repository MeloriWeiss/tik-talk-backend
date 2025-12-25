from ..rabbitmq.call_rpc import call_rpc


async def send_log(data: dict, log_type: str = "http"):
    await call_rpc(
        service_queue='logging_queue',
        message={
            'log_type': log_type,
            'data': data
        }
    )
