from pydantic import BaseModel


class CreatePostDTO(BaseModel):
    title: str = "",
    content: str = "",
    authorId: int = None,
    communityId: int = None