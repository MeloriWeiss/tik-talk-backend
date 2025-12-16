from pydantic import BaseModel


class DefaultResponse(BaseModel):
    error: bool
    message: str