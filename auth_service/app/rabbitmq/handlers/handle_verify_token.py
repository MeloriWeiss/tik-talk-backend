from ..utils.check_token_in_db import check_token_in_db
from ..utils.create_tokens import decode_token


async def handle_verify_token(data: dict):
    token = data.get("token")

    is_token_valid = await check_token_in_db(token)
    token_data = decode_token(token)

    return {
        "valid": is_token_valid,
        "token_data": token_data
    }