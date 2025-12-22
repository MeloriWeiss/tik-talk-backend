async def handle_log_critical(data: dict):
    log_level = data.get("log_level")

    if log_level is None:
        return None

    try:
        return {"log_level": log_level}
    except Exception as e:
        return None
