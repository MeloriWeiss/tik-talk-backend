from fastapi import Request, APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.responses import JSONResponse

from ...schemas.post_schema import PostSchemaAuthorless
from ...shared.default_response import default_content
from .dto.update_me_dto import UpdateMeDTO
from ...database import get_async_session
from ...models.models import Account, Post
from ...schemas.account_schema import AccountSchema, ShortAccountSchema
from ...shared.errors.exceptions.not_found_exception import NotFoundException
from ...shared.errors.exceptions.unauthorized_exception import UnauthorizedException
from ...utils.check_auth import check_auth
from ...utils.serialize_datetime import serialize_datetime

accounts_router = APIRouter(prefix="/account", tags=["Account"])


@accounts_router.get("/me")
async def get_me(request: Request, session: AsyncSession = Depends(get_async_session)):
    token_data = (await check_auth(request)).get("token_data")

    account_id = token_data.get("account_id")

    if not account_id:
        raise UnauthorizedException("Invalid token")

    me_result = await session.execute(select(Account).options(
        joinedload(Account.posts).joinedload(Post.comments)
    ).where(Account.id == account_id))
    account = me_result.unique().scalar_one_or_none()

    if not account:
        raise NotFoundException(detail="Account not found")

    serialized_account = AccountSchema[PostSchemaAuthorless].model_validate(account)

    return JSONResponse({"account": serialize_datetime(serialized_account.model_dump())})


@accounts_router.patch("/me")
async def update_me(update_me_dto: UpdateMeDTO, request: Request, session: AsyncSession = Depends(get_async_session)):
    token_data = (await check_auth(request)).get("token_data")

    account_id = token_data.get("account_id")

    if not account_id:
        raise UnauthorizedException("Invalid token")

    account_result = await session.execute(select(Account).options(
        joinedload(Account.posts)
    ).where(Account.id == account_id))
    account = account_result.unique().scalar_one_or_none()

    if not account:
        raise NotFoundException(detail="Account not found")

    for key, value in update_me_dto.__dict__.items():
        setattr(account, key, value)

    await session.commit()

    serialized_account = serialize_datetime(ShortAccountSchema.model_validate(account).model_dump())

    return JSONResponse({"account": serialized_account})


@accounts_router.get("/")
async def get_accounts(request: Request, session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    accounts_result = await session.execute(select(Account))
    accounts = accounts_result.scalars().all()

    serialized_accounts = [
        serialize_datetime(ShortAccountSchema.model_validate(account, from_attributes=True).model_dump()) for account in
        accounts]

    return JSONResponse({"accounts": serialized_accounts})


@accounts_router.get("/{account_id}")
async def get_account(account_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    account_result = await session.execute(select(Account).options(
        joinedload(Account.posts).joinedload(Post.comments)
    ).where(Account.id == account_id))
    account = account_result.unique().scalar_one_or_none()

    if not account:
        raise NotFoundException(detail="Account not found")

    serialized_account = AccountSchema[PostSchemaAuthorless].model_validate(account)

    return JSONResponse({"account": serialize_datetime(serialized_account.model_dump())})


@accounts_router.get("/subscribers/{account_id}")
async def get_subscriptions(account_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    account_result = await session.execute(select(Account).options(
        joinedload(Account.subscribers)
    ).where(Account.id == account_id))
    account = account_result.unique().scalar_one_or_none()

    if not account:
        raise NotFoundException(detail="Account not found")

    serialized_subscribers = [
        serialize_datetime(ShortAccountSchema.model_validate(subscriber, from_attributes=True).model_dump()) for
        subscriber in account.subscribers]

    return JSONResponse({"subscribers": serialized_subscribers})


@accounts_router.get("/subscriptions/{account_id}")
async def get_subscriptions(account_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    account_result = await session.execute(select(Account).options(
        joinedload(Account.subscriptions)
    ).where(Account.id == account_id))
    account = account_result.unique().scalar_one_or_none()

    if not account:
        raise NotFoundException(detail="Account not found")

    serialized_subscriptions = [
        serialize_datetime(ShortAccountSchema.model_validate(subscription, from_attributes=True).model_dump()) for
        subscription in account.subscriptions]

    return JSONResponse({"subscriptions": serialized_subscriptions})


@accounts_router.post("/subscribe/{user_id}")
async def subscribe(user_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    token_data = (await check_auth(request)).get("token_data")

    account_id = token_data.get("account_id")

    if not account_id:
        raise UnauthorizedException("Invalid token")

    me_result = await session.execute(select(Account).options(
        joinedload(Account.subscribers)
    ).where(Account.id == account_id))
    me = me_result.unique().scalar_one_or_none()

    if not me:
        raise NotFoundException(detail="Account not found")

    account_result = await session.execute(select(Account).options(
        joinedload(Account.subscribers)
    ).where(Account.id == user_id))
    account = account_result.unique().scalar_one_or_none()

    if me in account.subscribers:
        return JSONResponse(content=default_content(message="Already subscribed"))

    account.subscribers.append(me)

    await session.commit()

    return JSONResponse(content=default_content(message="Successfully subscribed"))


@accounts_router.delete("/subscribe/{user_id}")
async def unsubscribe(user_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    token_data = (await check_auth(request)).get("token_data")

    account_id = token_data.get("account_id")

    if not account_id:
        raise UnauthorizedException("Invalid token")

    me_result = await session.execute(select(Account).options(
        joinedload(Account.subscribers)
    ).where(Account.id == account_id))
    me = me_result.unique().scalar_one_or_none()

    if not me:
        raise NotFoundException(detail="Account not found")

    account_result = await session.execute(select(Account).options(
        joinedload(Account.subscribers)
    ).where(Account.id == user_id))
    account = account_result.unique().scalar_one_or_none()

    if me not in account.subscribers:
        return JSONResponse(content=default_content(message="Already unsubscribed"))

    account.subscribers.remove(me)

    await session.commit()

    return JSONResponse(content=default_content(message="Successfully unsubscribed"))
