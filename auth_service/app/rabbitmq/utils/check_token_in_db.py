from datetime import datetime, timezone

from sqlalchemy import select

from ...utils.string_hash import get_string_hash
from ...database import async_session
from ...models.models import Token


async def check_token_in_db(token: str) -> bool:
    async with async_session() as session:
        hashed_token = get_string_hash(token)

        result_token = await session.execute(
            select(Token).where(
                Token.hashed_token == hashed_token
            )
        )
        existing_token: Token = result_token.scalar_one_or_none()

        if existing_token is None:
            return False

        if existing_token.revoked or existing_token.expires_at <= datetime.now(timezone.utc):
            await session.delete(existing_token)
            await session.commit()
            return False

        return True