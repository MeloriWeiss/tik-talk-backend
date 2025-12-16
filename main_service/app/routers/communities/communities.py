from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.requests import Request
from starlette.responses import JSONResponse

from .dto.communities_filters_dto import CommunitiesFiltersDto
from .dto.community_create_dto import CommunityCreateDTO
from ...database import get_async_session
from ...models.models import Community, Author, AuthorType
from ...schemas.community_schema import CommunityShema, ShortCommunitySchema, PostCommunitySchemaAuthorless
from ...shared.exceptions.not_found_exception import NotFoundException
from ...shared.exceptions.unauthorized_exception import UnauthorizedException
from ...utils.check_auth import check_auth

communities_router = APIRouter(prefix="/community", tags=["Community"])

@communities_router.get("/")
async def get_communities(request: Request, filters: CommunitiesFiltersDto = Depends(), session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    communities_query = select(Community).options(
        joinedload(Community.admin)
    )

    if filters.name:
        communities_query.filter(Community.name.ilike(f"%{filters.name}%"))

    if filters.themes:
        communities_query.filter(Community.themes.overlap(filters.themes))

    if filters.tags:
        communities_query.filter(Community.tags.overlap(filters.tags))

    if filters.page and filters.size:
        communities_query.offset((filters.page - 1) * filters.size).limit(filters.size)

    communities_result = await session.execute(communities_query)
    communities = communities_result.scalars().all()

    serialized_communities = [ShortCommunitySchema.model_validate(community, from_attributes=True).model_dump() for community in
                           communities]

    return JSONResponse({"communities": serialized_communities})

@communities_router.get("/{community_id}")
async def get_community(community_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    community_result = await session.execute(select(Community).options(
        joinedload(Community.admin),
        joinedload(Community.posts)
    ).where(Community.id == community_id))
    community = community_result.unique().scalar_one_or_none()

    if not community:
        raise NotFoundException(detail="Community not found")

    serialized_community = CommunityShema.model_validate(community, from_attributes=True)
    validated_posts = [PostCommunitySchemaAuthorless.model_validate(post, from_attributes=True).model_dump() for post in
                       serialized_community.posts]

    serialized_community.posts = validated_posts

    return JSONResponse({"community": serialized_community.model_dump()})

@communities_router.post("/")
async def create_community(community_create_data: CommunityCreateDTO, request: Request, session: AsyncSession = Depends(get_async_session)):
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
        type=AuthorType.community,
        community=new_community,
    )
    session.add(new_community_author)
    await session.commit()

    serialized_community = CommunityShema.model_validate(new_community_author, from_attributes=True)
    validated_posts = [PostCommunitySchemaAuthorless.model_validate(post, from_attributes=True).model_dump() for post in
                       serialized_community.posts]

    serialized_community.posts = validated_posts

    return JSONResponse({"community": serialized_community.model_dump()}, status_code=201)