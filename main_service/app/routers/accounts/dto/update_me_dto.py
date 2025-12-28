from typing import Optional

from pydantic import BaseModel


class UpdateMeDTO(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    stack: Optional[list[str]]
    city: Optional[str]
    description: Optional[str]
