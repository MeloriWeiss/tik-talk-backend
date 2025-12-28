from fastapi import APIRouter, Depends
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.requests import Request
from starlette.responses import JSONResponse

from .utils.get_existing_chat import get_existing_chat
from ...database import get_async_session
from ...models.models import Chat
from ...schemas.chat_schema import ShortChatSchema
from ...shared.errors.exceptions.unauthorized_exception import UnauthorizedException
from ...utils.check_auth import check_auth
from ...utils.serialize_datetime import serialize_datetime

chats_router = APIRouter(prefix="/chat", tags=["Chat"])


@chats_router.get("/get_my_chats")
async def get_chats(request: Request, session: AsyncSession = Depends(get_async_session)):
    token_data = (await check_auth(request)).get("token_data")

    account_id = token_data.get("account_id")

    if not account_id:
        raise UnauthorizedException("Invalid token")

    chats_result = await session.execute(select(Chat).options(
        joinedload(Chat.userFirst),
        joinedload(Chat.userSecond),
        joinedload(Chat.messages)
    ))
    chats = chats_result.unique().scalars().all()

    serialized_chats: list[ShortChatSchema] = []

    for chat in chats:
        last_message = chat.messages[-1].text if len(chat.messages) else None

        chat.message = last_message

        user_from = chat.userSecond if chat.userFirstId == account_id else chat.userFirst
        chat.userFrom = user_from

        chat.unreadMessages = 0

        serialized_chats.append(serialize_datetime(ShortChatSchema.model_validate(chat).model_dump()))

    return JSONResponse({"chats": serialized_chats})


@chats_router.post("/{user_id}")
async def create_or_get_chat(user_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    token_data = (await check_auth(request)).get("token_data")

    account_id = token_data.get("account_id")

    if not account_id:
        raise UnauthorizedException("Invalid token")

    serialized_chat = await get_existing_chat(account_id, user_id, session)

    if not serialized_chat:
        new_chat = Chat(
            userFirstId=account_id,
            userSecondId=user_id,
        )
        session.add(new_chat)
        await session.commit()

        serialized_chat = await get_existing_chat(account_id, user_id, session)

    return JSONResponse({"chat": serialized_chat})
