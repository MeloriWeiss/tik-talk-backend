from pydantic import BaseModel

class PostAccountSchemaAuthorless(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True


class AccountSchema(BaseModel):
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
    # createdAt: datetime
    # updatedAt: datetime
    #
    # comments: list
    posts: list[PostAccountSchemaAuthorless]

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
    # createdAt: datetime
    # updatedAt: datetime
    #
    # comments: list

    class Config:
        from_attributes = True