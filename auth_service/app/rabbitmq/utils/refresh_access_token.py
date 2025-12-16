from .create_tokens import create_token
from ..utils.delete_tokens import delete_token


async def refresh_access_token(account_id: int):
    await delete_token(account_id, "access")
    token = await create_token({"account_id": account_id})

    if not token:
        return None

    return token