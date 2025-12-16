from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..dto.create_post_dto import CreatePostDto
from ....database import async_session
from ....models.models import Author, Post, AuthorType, Community
from ....schemas.community_schema import ShortCommunitySchemaAdminless
from ....schemas.post_schema import ShortPostCommunitySchemaAdminless
from ....shared.exceptions.not_found_exception import NotFoundException


async def create_community_post(create_post_data: CreatePostDto):
    async with async_session() as session:
        community_result = await session.execute(select(Community).options(
            joinedload(Community.author).joinedload(Author.community)
        ).where(Community.id == create_post_data.communityId))
        community = community_result.unique().scalar_one_or_none()

        if not community:
            raise NotFoundException(detail="Community not found")

        author = community.author

        if not author:
            raise NotFoundException(detail="Author not found")

        new_post = Post(
            title=create_post_data.title,
            content=create_post_data.content,
            author_type=AuthorType.community,
            author_id=author.id,
        )
        session.add(new_post)
        await session.commit()

        serialized_post = ShortPostCommunitySchemaAdminless.model_validate(new_post, from_attributes=True)
        validated_community = ShortCommunitySchemaAdminless.model_validate(new_post.author.community,
                                                                           from_attributes=True)

        serialized_post.author = validated_community.model_dump()

        return serialized_post
