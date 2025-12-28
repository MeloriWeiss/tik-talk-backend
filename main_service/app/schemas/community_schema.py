from datetime import datetime
from typing import Optional, TypeVar, Generic

from pydantic import BaseModel

from .account_schema import ShortAccountSchema

PostT = TypeVar('PostT')

class CommunityShema(BaseModel, Generic[PostT]):
    id: int
    name: str
    admin: ShortAccountSchema
    themes: list[str]
    tags: list[str]
    bannerUrl: Optional[str]
    avatarUrl: Optional[str]
    description: Optional[str]
    subscribersAmount: int
    createdAt: datetime
    isJoined: bool
    posts: list[PostT]

    class Config:
        from_attributes = True


class ShortCommunitySchema(BaseModel):
    id: int
    name: str
    admin: ShortAccountSchema
    themes: list[str]
    tags: list[str]
    bannerUrl: Optional[str]
    avatarUrl: Optional[str]
    description: Optional[str]
    subscribersAmount: int
    createdAt: datetime
    isJoined: bool

    class Config:
        from_attributes = True


class ShortCommunitySchemaAdminless(BaseModel):
    id: int
    name: str
    themes: list[str]
    tags: list[str]
    bannerUrl: Optional[str]
    avatarUrl: Optional[str]
    description: Optional[str]
    subscribersAmount: int
    createdAt: datetime
    isJoined: bool

    class Config:
        from_attributes = True