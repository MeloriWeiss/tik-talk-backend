from .create_tokens import create_tokens
from .delete_tokens import delete_tokens

async def update_tokens(account_id: int):
    await delete_tokens(account_id)
    tokens = await create_tokens({"account_id": account_id})

    return tokens
