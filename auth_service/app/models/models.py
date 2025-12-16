from sqlalchemy import Column, Integer, String, Enum, Boolean, TIMESTAMP
import enum
from datetime import datetime, timezone

from .base import AuthBase


class TokenType(str, enum.Enum):
    access = "access"
    refresh = "refresh"


class Token(AuthBase):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, nullable=False)
    hashed_token = Column(String, unique=True, nullable=False)
    token_type = Column(Enum(TokenType), nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    revoked = Column(Boolean, default=False)
