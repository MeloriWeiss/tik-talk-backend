from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..dto.create_post_dto import CreatePostDTO
from ....database import async_session
from ....models.models import Author, Post, AuthorType, Community
from ....schemas.author_schema import ShortAuthorCommunitySchemaAdminless
from ....schemas.post_schema import PostSchemaAuthorAdminless
from ....shared.errors.exceptions.not_found_exception import NotFoundException
from ....utils.serialize_datetime import serialize_datetime


async def create_community_post(create_post_data: CreatePostDTO):
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
            author_type=AuthorType.COMMUNITY,
            author_id=author.id,
        )
        session.add(new_post)
        await session.commit()

        result = await session.execute(select(Post).options(
            joinedload(Post.comments),
            joinedload(Post.author).joinedload(Author.account)
        ).where(Post.id == new_post.id))
        post = result.unique().scalar_one_or_none()

        if not post:
            raise NotFoundException("Post not found")

        serialized_post = PostSchemaAuthorAdminless[ShortAuthorCommunitySchemaAdminless].model_validate(post)
        serialized_post.author = serialized_post.author.community.model_dump()

        return serialize_datetime(serialized_post.model_dump())
