from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.requests import Request
from starlette.responses import JSONResponse

from .dto.create_post_dto import CreatePostDto
from .utils.create_account_post import create_account_post
from .utils.create_community_post import create_community_post
from ...database import get_async_session
from ...models.models import Post, Author, Account
from ...schemas.account_schema import ShortAccountSchema, PostAccountSchemaAuthorless
from ...schemas.post_schema import ShortPostAccountSchema
from ...shared.errors.exceptions.bad_request_exception import BadRequestException
from ...shared.errors.exceptions.not_found_exception import NotFoundException
from ...utils.check_auth import check_auth

posts_router = APIRouter(prefix="/post", tags=["Post"])


@posts_router.get("/")
async def get_posts(request: Request, account_id: int = Query(None),
                    session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    account_result = await session.execute(select(Account).options(
        joinedload(Account.posts)
    ).where(Account.id == account_id))
    account = account_result.unique().scalar_one_or_none()

    if not account:
        raise NotFoundException(detail="Account not found")

    validated_posts = [PostAccountSchemaAuthorless.model_validate(post, from_attributes=True).model_dump() for post in
                       account.posts]

    return JSONResponse({"posts": validated_posts})


@posts_router.get("/{post_id}")
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).options(
        joinedload(Post.author).joinedload(Author.account)
    ).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise NotFoundException("Post not found")

    serialized_post = ShortPostAccountSchema.model_validate(post, from_attributes=True)
    validated_account = ShortAccountSchema.model_validate(post.author.account, from_attributes=True)

    serialized_post.author = validated_account.model_dump()

    return JSONResponse({"post": serialized_post.model_dump()})


@posts_router.post("/")
async def create_post(create_post_data: CreatePostDto, request: Request):
    await check_auth(request)

    serialized_post = None

    if type(create_post_data.authorId) is not int and type(create_post_data.communityId) is not int:
        raise BadRequestException(detail="Author or community are required")

    if type(create_post_data.authorId) is int:
        serialized_post = await create_account_post(create_post_data)

    elif type(create_post_data.communityId) is int:
        serialized_post = await create_community_post(create_post_data)

    return JSONResponse({"post": serialized_post.model_dump()}, status_code=201)
