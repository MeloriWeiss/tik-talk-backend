from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .account_schema import ShortAccountSchema
from .message_schema import MessageSchema


class ChatSchema(BaseModel):
    id: int
    userFirst: ShortAccountSchema
    userSecond: ShortAccountSchema
    messages: list[MessageSchema]

    class Config:
        from_attributes = True

class ShortChatSchema(BaseModel):
    id: int
    userFrom: ShortAccountSchema
    message: Optional[str]
    createdAt: datetime
    unreadMessages: int

    class Config:
        from_attributes = True