from ..utils.update_tokens import update_tokens


async def handle_login(data: dict):
    account_id = data.get("account_id")

    if account_id is None:
        return None

    try:
        tokens = await update_tokens(account_id)
        return tokens
    except Exception as e:
        return None