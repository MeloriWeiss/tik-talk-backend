def default_content(message: str, has_error: bool = False):
    return {"error": has_error, "message": message}