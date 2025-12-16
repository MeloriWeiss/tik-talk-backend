from pydantic import BaseModel


class CreatePostDto(BaseModel):
    title: str = "",
    content: str = "",
    authorId: int = None,
    communityId: int = None