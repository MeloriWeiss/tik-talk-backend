from datetime import datetime

from pydantic import BaseModel


class HttpLogSchema(BaseModel):
    id: int
    level: str
    timestamp: str
    service: str
    request_id: str
    method: str
    path: str
    status_code: int
    duration_ms: float
    client_ip: str
    message: str
    createdAt: datetime

    class Config:
        from_attributes = True
