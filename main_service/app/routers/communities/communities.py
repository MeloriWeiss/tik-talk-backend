from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.requests import Request
from starlette.responses import JSONResponse

from .dto.communities_filters_dto import CommunitiesFiltersDTO
from .dto.community_create_dto import CommunityCreateDTO
from .dto.update_community_dto import UpdateCommunityDTO
from ...database import get_async_session
from ...models.models import Community, Author, AuthorType, Post, Comment
from ...schemas.community_schema import CommunityShema, ShortCommunitySchema
from ...schemas.post_schema import PostSchemaAuthorless
from ...shared.default_response import default_content
from ...shared.errors.exceptions.forbidden_exception import ForbiddenException
from ...shared.errors.exceptions.not_found_exception import NotFoundException
from ...shared.errors.exceptions.unauthorized_exception import UnauthorizedException
from ...utils.check_auth import check_auth
from ...utils.serialize_datetime import serialize_datetime

communities_router = APIRouter(prefix="/community", tags=["Community"])


@communities_router.get("/")
async def get_communities(request: Request, filters: CommunitiesFiltersDTO = Depends(),
                          session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    communities_query = select(Community).options(
        joinedload(Community.admin)
    )
    print(filters, flush=True)
    if filters.name:
        communities_query = communities_query.filter(Community.name.ilike(f"%{filters.name}%"))

    if filters.themes:
        communities_query = communities_query.filter(Community.themes.overlap(filters.themes))

    if filters.tags:
        communities_query = communities_query.filter(Community.tags.overlap(filters.tags))

    communities_query = communities_query.offset((filters.page - 1) * filters.size).limit(filters.size)

    communities_result = await session.execute(communities_query)
    communities = communities_result.scalars().all()

    serialized_communities = [
        serialize_datetime(ShortCommunitySchema.model_validate(community, from_attributes=True).model_dump()) for
        community in
        communities]

    return JSONResponse({"communities": serialized_communities})


@communities_router.get("/{community_id}")
async def get_community(community_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    community_result = await session.execute(select(Community).options(
        joinedload(Community.admin),
        joinedload(Community.posts).joinedload(Post.comments).joinedload(Comment.author)
    ).where(Community.id == community_id))
    community = community_result.unique().scalar_one_or_none()

    if not community:
        raise NotFoundException(detail="Community not found")

    serialized_community = CommunityShema[PostSchemaAuthorless].model_validate(community, from_attributes=True)

    result_community = serialize_datetime(serialized_community.model_dump())

    return JSONResponse({"community": result_community})


@communities_router.post("/")
async def create_community(community_create_data: CommunityCreateDTO, request: Request,
                           session: AsyncSession = Depends(get_async_session)):
    token_data = (await check_auth(request)).get("token_data")

    account_id = token_data.get("account_id")

    if not account_id:
        raise UnauthorizedException("Invalid token")

    new_community = Community(
        admin_id=account_id,
        name=community_create_data.name,
        description=community_create_data.description,
        tags=community_create_data.tags,
        themes=community_create_data.themes,
    )
    session.add(new_community)
    await session.flush()

    new_community_author = Author(
        type=AuthorType.COMMUNITY,
        community=new_community,
    )
    session.add(new_community_author)
    await session.commit()

    community_result = await session.execute(select(Community).options(
        joinedload(Community.admin),
        joinedload(Community.posts)
    ).where(Community.id == new_community.id))
    community = community_result.unique().scalar_one_or_none()

    serialized_community = serialize_datetime(CommunityShema[PostSchemaAuthorless].model_validate(community).model_dump())

    return JSONResponse({"community": serialized_community}, status_code=201)


@communities_router.patch('/{community_id}')
async def update_community(community_id: int, update_community_dto: UpdateCommunityDTO, request: Request,
                           session: AsyncSession = Depends(get_async_session)):
    token_data = (await check_auth(request)).get("token_data")

    account_id = token_data.get("account_id")

    if not account_id:
        raise UnauthorizedException("Invalid token")

    community_result = await session.execute(select(Community).options(
        joinedload(Community.admin),
        joinedload(Community.posts).joinedload(Post.comments).joinedload(Comment.author)
    ).where(Community.id == community_id))
    community = community_result.unique().scalar_one_or_none()

    if not community:
        raise NotFoundException(detail="Community not found")

    if community.admin.id != account_id:
        raise ForbiddenException(detail="It is not your community")

    for key, value in update_community_dto.__dict__.items():
        setattr(community, key, value)

    await session.commit()

    serialized_community = serialize_datetime(CommunityShema[PostSchemaAuthorless].model_validate(community).model_dump())

    return JSONResponse({"community": serialized_community})

@communities_router.delete("/{community_id}")
async def delete_community(community_id: int, session: AsyncSession = Depends(get_async_session)):
    community_result = await session.execute(select(Community).where(Community.id == community_id))
    community = community_result.scalar_one_or_none()

    if not community:
        raise NotFoundException(detail="Community not found")

    await session.delete(community)
    await session.commit()

    return JSONResponse(content=default_content("Community successfully deleted"))