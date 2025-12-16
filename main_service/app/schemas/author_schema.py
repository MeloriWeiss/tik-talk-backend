from pydantic import BaseModel

from .account_schema import AccountSchema, ShortAccountSchema
from .community_schema import CommunityShema, ShortCommunitySchema, ShortCommunitySchemaAdminless


class AuthorAccountSchema(BaseModel):
    id: int
    type: str
    account: AccountSchema | None

    class Config:
        from_attributes = True

class ShortAuthorAccountSchema(BaseModel):
    id: int
    type: str
    account: ShortAccountSchema | None

    class Config:
        from_attributes = True


class AuthorCommunitySchema(BaseModel):
    id: int
    type: str
    community: CommunityShema | None

    class Config:
        from_attributes = True

class ShortAuthorCommunitySchema(BaseModel):
    id: int
    type: str
    community: ShortCommunitySchema | None

    class Config:
        from_attributes = True

class ShortAuthorCommunitySchemaAdminless(BaseModel):
    id: int
    type: str
    community: ShortCommunitySchemaAdminless | None

    class Config:
        from_attributes = True