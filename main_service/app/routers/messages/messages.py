from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse

from ...database import get_async_session
from ...models.models import Message
from ...schemas.message_schema import MessageSchema
from ...shared.errors.exceptions.unauthorized_exception import UnauthorizedException
from ...utils.check_auth import check_auth
from ...utils.serialize_datetime import serialize_datetime

messages_router = APIRouter(prefix="/message", tags=["Message"])


@messages_router.post('/send/{chat_id}')
async def send_message(chat_id: int, request: Request, message: str = Query(None),
                       session: AsyncSession = Depends(get_async_session)):
    token_data = (await check_auth(request)).get("token_data")

    account_id = token_data.get("account_id")

    if not account_id:
        raise UnauthorizedException("Invalid token")

    message = Message(
        userFromId=account_id,
        personalChatId=chat_id,
        text=message,
        chatId=chat_id,
    )
    session.add(message)
    await session.commit()

    serialized_message = serialize_datetime(MessageSchema.model_validate(message).model_dump())

    return JSONResponse({"message": serialized_message})
