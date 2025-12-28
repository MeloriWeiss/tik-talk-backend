from typing import Optional

from pydantic import BaseModel


class UpdateCommunityDTO(BaseModel):
    name: Optional[str]
    themes: Optional[list[str]]
    tags: Optional[list[str]]
    description: Optional[str]