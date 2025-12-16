from ..utils.create_tokens import create_tokens


async def handle_register(data: dict):
    account_id = data.get("account_id")

    if account_id is None:
        return None

    try:
        tokens = await create_tokens({"account_id": account_id})
        return tokens
    except Exception as e:
        return None
