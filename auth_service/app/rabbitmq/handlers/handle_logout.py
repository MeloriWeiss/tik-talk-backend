from ..utils.create_tokens import decode_token
from ..utils.delete_tokens import delete_tokens
from ..utils.default_return_results import success


async def handle_logout(data: dict):
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
        await delete_tokens(account_id)
        return success(True)
    except Exception as e:
        return success(False)
