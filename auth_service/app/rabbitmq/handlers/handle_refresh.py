from ..utils.create_tokens import decode_token
from ..utils.refresh_access_token import refresh_access_token
from ..utils.default_return_results import success


async def handle_refresh(data: dict):
    token = data.get('token')

    if not token:
        return success(False)

    decoded_token = decode_token(token)

    if not decoded_token:
        return success(False)

    account_id = decoded_token.get('account_id')

    if not account_id:
        return success(False)

    try:
        result = await refresh_access_token(account_id)
        return result
    except Exception as e:
        return success(False)
