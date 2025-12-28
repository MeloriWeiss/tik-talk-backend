from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from ....models.models import Chat
from ....schemas.chat_schema import ChatSchema
from ....utils.serialize_datetime import serialize_datetime


async def get_existing_chat(account_id: int, user_id: int, session: AsyncSession):
    existing_chat_result = await session.execute(select(Chat).options(
        joinedload(Chat.userFirst),
        joinedload(Chat.userSecond),
        joinedload(Chat.messages)
    ).where(
        or_(
            and_(
                Chat.userFirstId == account_id,
                Chat.userSecondId == user_id
            ),
            and_(
                Chat.userFirstId == user_id,
                Chat.userSecondId == account_id
            )
        )
    ))
    chat = existing_chat_result.unique().scalar_one_or_none()

    if not chat:
        return None

    return serialize_datetime(ChatSchema.model_validate(chat).model_dump())
