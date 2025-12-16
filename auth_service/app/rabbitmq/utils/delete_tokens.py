from sqlalchemy import delete

from ...database import async_session
from ...models.models import Token


async def delete_tokens(account_id: int):
    async with async_session() as session:
        await session.execute(delete(Token).where(
            Token.account_id == account_id
        ))
        await session.commit()


async def delete_token(account_id: int, token_type: str):
    async with async_session() as session:
        await session.execute(delete(Token).where(
            Token.account_id == account_id,
            Token.token_type == token_type
        ))
        await session.commit()