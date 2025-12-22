from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from ...database import get_async_session
from ...routers.auth.dto.login_dto import LoginDto
from ...models.models import Account, Author, AuthorType
from ...rabbitmq.call_rpc import call_rpc
from ...shared.default_response import default_content
from ...shared.errors.exceptions.bad_request_exception import BadRequestException
from ...shared.errors.exceptions.not_found_exception import NotFoundException
from ...shared.errors.exceptions.unauthorized_exception import UnauthorizedException
from ...utils.cookie_utils import set_tokens_cookie, delete_tokens_cookie
from ...utils.password_hash import get_password_hash, verify_hashed_password

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login")
async def login(login_data: LoginDto, response: Response, session: AsyncSession = Depends(get_async_session)):
    account_result = await session.execute(select(Account).where(Account.username == login_data.username))
    account = account_result.scalars().first()

    if not account:
        raise NotFoundException(detail="Account not found")

    if not verify_hashed_password(login_data.password, account.hashed_password):
        raise NotFoundException(detail="Incorrect password")

    result = await call_rpc(
        service_queue='auth_queue',
        message={'action': 'login', 'account_id': account.id},
    )

    if not result or not result.get('access_token') or not result.get('refresh_token'):
        raise UnauthorizedException(detail="Invalid token")

    set_tokens_cookie(response, result)

    return JSONResponse(
        status_code=200,
        headers=response.headers,
        content=default_content(has_error=False, message="Successfully logged in")
    )


@auth_router.post("/register")
async def register(login_data: LoginDto, response: Response, session: AsyncSession = Depends(get_async_session)):
    result_account = await session.execute(select(Account).where(Account.username == login_data.username))
    existing_account = result_account.scalars().first()

    if existing_account:
        raise BadRequestException(detail="Username already exists")

    hashed_password = get_password_hash(login_data.password)

    new_account = Account(username=login_data.username, hashed_password=hashed_password)
    session.add(new_account)
    await session.flush()

    author = Author(
        type=AuthorType.account,
        account=new_account,
    )
    session.add(author)
    await session.commit()

    if not author:
        raise BadRequestException(detail="Can't register with this account")

    result = await call_rpc(
        service_queue='auth_queue',
        message={'action': 'register', 'account_id': new_account.id},
    )

    if not result or not result.get('access_token') or not result.get('refresh_token'):
        raise UnauthorizedException(detail="Invalid token")

    set_tokens_cookie(response, result)

    return JSONResponse(
        status_code=200,
        headers=response.headers,
        content=default_content(has_error=False, message="Successfully registered")
    )


@auth_router.get("/logout")
async def logout(request: Request, response: Response):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if not access_token or not refresh_token:
        raise UnauthorizedException(detail="Unauthorized: missing tokens")

    result = await call_rpc(
        service_queue='auth_queue',
        message={'action': 'logout', 'token': access_token},
    )

    delete_tokens_cookie(response)

    if not result or not result.get('success'):
        raise UnauthorizedException(detail="Error logging out")

    return JSONResponse(
        status_code=200,
        headers=response.headers,
        content=default_content(has_error=False, message="Successfully logged out")
    )


@auth_router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise UnauthorizedException(detail="Unauthorized: missing tokens")

    result = await call_rpc(
        service_queue='auth_queue',
        message={'action': 'refresh', 'token': refresh_token},
    )

    set_tokens_cookie(response, result)

    return JSONResponse(
        status_code=200,
        headers=response.headers,
        content=default_content(has_error=False, message="Successfully refreshed")
    )
