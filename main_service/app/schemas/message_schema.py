from datetime import datetime

from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: int
    userFromId: int
    personalChatId: int
    text: str
    isRead: bool
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True