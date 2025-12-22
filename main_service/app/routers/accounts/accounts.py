from fastapi import Request, APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.responses import JSONResponse

from ...database import get_async_session
from ...models.models import Account
from ...schemas.account_schema import AccountSchema, ShortAccountSchema, PostAccountSchemaAuthorless
from ...shared.errors.exceptions.not_found_exception import NotFoundException
from ...utils.check_auth import check_auth

accounts_router = APIRouter(prefix="/account", tags=["Account"])


@accounts_router.get("/")
async def get_accounts(request: Request, session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    accounts_result = await session.execute(select(Account))
    accounts = accounts_result.scalars().all()

    serialized_accounts = [ShortAccountSchema.model_validate(account, from_attributes=True).model_dump() for account in
                           accounts]

    return JSONResponse({"accounts": serialized_accounts})


@accounts_router.get("/{account_id}")
async def get_account(account_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    account_result = await session.execute(select(Account).options(
        joinedload(Account.posts)
    ).where(Account.id == account_id))
    account = account_result.unique().scalar_one_or_none()

    if not account:
        raise NotFoundException(detail="Account not found")

    serialized_account = AccountSchema.model_validate(account, from_attributes=True)
    validated_posts = [PostAccountSchemaAuthorless.model_validate(post, from_attributes=True).model_dump() for post in
                       serialized_account.posts]

    serialized_account.posts = validated_posts

    return JSONResponse({"account": serialized_account.model_dump()})


@accounts_router.get("/subscribers/{account_id}")
async def get_subscriptions(account_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    account_result = await session.execute(select(Account).options(
        joinedload(Account.subscribers)
    ).where(Account.id == account_id))
    account = account_result.unique().scalar_one_or_none()

    if not account:
        raise NotFoundException(detail="Account not found")

    serialized_subscribers = [ShortAccountSchema.model_validate(subscriber, from_attributes=True).model_dump() for
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

    serialized_subscriptions = [ShortAccountSchema.model_validate(subscription, from_attributes=True).model_dump() for
                                subscription in account.subscriptions]

    return JSONResponse({"subscriptions": serialized_subscriptions})
