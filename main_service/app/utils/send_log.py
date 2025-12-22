from ..rabbitmq.call_rpc import call_rpc


async def send_log(data: str, log_type: str = "info"):
    await call_rpc(
        service_queue='logging_queue',
        message={'log_type': log_type, 'data': data}
    )
