from datetime import timedelta, datetime, timezone

import jwt

from ...utils.string_hash import get_string_hash
from ...database import async_session
from ...models.models import Token

ACCESS_TOKEN_LIFETIME = 15
REFRESH_TOKEN_LIFETIME = 7

SECRET_KEY = "SDFJLWERPIUVCBCXVM"
ALGORITHM = "HS256"


async def create_tokens(data: dict):
    access_token, access_expire_date = create_access_token(data)
    refresh_token, refresh_expire_date = create_refresh_token(data)

    account_id = data.get('account_id')

    if account_id is None:
        return None

    await save_token(account_id, access_token, 'access', access_expire_date)
    await save_token(account_id, refresh_token, 'refresh', refresh_expire_date)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

async def create_token(data: dict):
    access_token, access_expire_date = create_access_token(data)

    account_id = data.get('account_id')

    if account_id is None:
        return None

    await save_token(account_id, access_token, 'access', access_expire_date)

    return {
        "access_token": access_token
    }


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_LIFETIME)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt, expire


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=REFRESH_TOKEN_LIFETIME)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt, expire


async def save_token(account_id: int, token: str, token_type: str, expires_at: datetime):
    async with async_session() as session:
        token_record = Token(
            account_id=account_id,
            hashed_token=get_string_hash(token),
            token_type=token_type,
            expires_at=expires_at,
            created_at=datetime.now(timezone.utc),
        )
        session.add(token_record)
        await session.commit()

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None