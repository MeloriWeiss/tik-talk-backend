from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean

from .base import ChatsBase


class Chat(ChatsBase):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, index=True)
    userFrom = Column(String, nullable=False)
    message = Column(String, nullable=False)
    unreadMessages = Column(Integer, default=0)

    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updatedAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))

class Message(ChatsBase):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    userFromId = Column(Integer, nullable=False)
    personalChatId = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    isRead = Column(Boolean, default=False)

    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updatedAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))