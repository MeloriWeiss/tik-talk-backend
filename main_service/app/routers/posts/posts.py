from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.requests import Request
from starlette.responses import JSONResponse

from ...schemas.author_schema import ShortAuthorAccountSchema, ShortAuthorCommunitySchemaAdminless
from ...schemas.post_schema import PostSchemaAuthorless, PostSchema
from ...shared.default_response import default_content
from .dto.create_post_dto import CreatePostDTO
from .utils.create_account_post import create_account_post
from .utils.create_community_post import create_community_post
from ...database import get_async_session
from ...models.models import Post, Author, Account
from ...shared.errors.exceptions.bad_request_exception import BadRequestException
from ...shared.errors.exceptions.not_found_exception import NotFoundException
from ...utils.check_auth import check_auth
from ...utils.serialize_datetime import serialize_datetime

posts_router = APIRouter(prefix="/post", tags=["Post"])


@posts_router.get("/")
async def get_posts(request: Request, account_id: int = Query(None),
                    session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    account_result = await session.execute(select(Account).options(
        joinedload(Account.posts).joinedload(Post.comments)
    ).where(Account.id == account_id))
    account = account_result.unique().scalar_one_or_none()

    if not account:
        raise NotFoundException(detail="Account not found")

    validated_posts = [serialize_datetime(PostSchemaAuthorless.model_validate(post).model_dump()) for post in
                       account.posts]

    return JSONResponse({"posts": validated_posts})


@posts_router.get("/{post_id}")
async def get_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).options(
        joinedload(Post.author).joinedload(Author.account),
        joinedload(Post.author).joinedload(Author.community),
        joinedload(Post.comments)
    ).where(Post.id == post_id))
    post = result.unique().scalar_one_or_none()

    if not post:
        raise NotFoundException("Post not found")

    serialized_post = None

    if post.author.account:
        serialized_post = PostSchema[ShortAuthorAccountSchema].model_validate(post)
        serialized_post.author = serialized_post.author.account.model_dump()

    elif post.author.community:
        serialized_post = PostSchema[ShortAuthorCommunitySchemaAdminless].model_validate(post)
        serialized_post.author = serialized_post.author.community.model_dump()

    return JSONResponse({"post": serialize_datetime(serialized_post.model_dump())})


@posts_router.post("/")
async def create_post(create_post_data: CreatePostDTO, request: Request):
    await check_auth(request)

    serialized_post = None

    if type(create_post_data.authorId) is not int and type(create_post_data.communityId) is not int:
        raise BadRequestException(detail="Author or community are required")

    if type(create_post_data.authorId) is int:
        serialized_post = await create_account_post(create_post_data)

    elif type(create_post_data.communityId) is int:
        serialized_post = await create_community_post(create_post_data)

    return JSONResponse({"post": serialized_post}, status_code=201)

@posts_router.delete("/{post_id}")
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    post_result = await session.execute(select(Post).where(Post.id == post_id))
    post = post_result.scalar_one_or_none()

    await session.delete(post)
    await session.commit()

    return JSONResponse(content=default_content("Post successfully deleted"))