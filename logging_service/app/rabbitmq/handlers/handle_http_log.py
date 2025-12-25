from ..utils.save_log import save_log


async def handle_http_log(data: dict):
    try:
        await save_log(data)
    except Exception as e:
        return None
