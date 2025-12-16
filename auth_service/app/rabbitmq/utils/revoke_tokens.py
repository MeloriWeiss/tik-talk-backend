from sqlalchemy import select

from ...database import async_session
from ...models.models import Token


async def revoke_tokens(account_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Token).filter(Token.account_id == account_id)
        )
        existing_tokens = result.scalars().all()

        access_token_obj: Token = next((token for token in existing_tokens if token.token_type == 'access'), None)
        refresh_token_obj: Token = next((token for token in existing_tokens if token.token_type == 'refresh'), None)

        if not access_token_obj or not refresh_token_obj:
            return True

        access_token_obj.revoked = True
        refresh_token_obj.revoked = True

        await session.commit()

        return True