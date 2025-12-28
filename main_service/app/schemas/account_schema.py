from datetime import datetime
from typing import TypeVar, Generic

from pydantic import BaseModel

PostT = TypeVar('PostT')


class AccountSchema(BaseModel, Generic[PostT]):
    id: int
    username: str
    avatar_url: str | None
    subscribersAmount: int
    firstName: str | None
    lastName: str | None
    isActive: bool
    stack: list[str]
    city: str | None
    description: str | None
    roles: list[str]
    createdAt: datetime
    updatedAt: datetime
    posts: list[PostT]

    class Config:
        from_attributes = True


class ShortAccountSchema(BaseModel):
    id: int
    username: str
    avatar_url: str | None
    subscribersAmount: int
    firstName: str | None
    lastName: str | None
    isActive: bool
    stack: list[str]
    city: str | None
    description: str | None
    roles: list[str]
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
