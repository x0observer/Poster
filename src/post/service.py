from fastapi import APIRouter, Depends, HTTPException
from middleware.engine import get_async_session
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.register import *
from src.post.contexts.post import PostBase, PostFull
from typing import Optional, List


from src.auth.contexts.permissons import UserPemissions, LOCAL_VISIBILITY_SCOPE


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_post(self, post: PostBase, active_user: UserPemissions) -> Post:
        print("__new_post__")
        new_post = Post(**post.dict(), user_id=active_user.id)
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post)
        print("__out_stock__")
        return new_post

    async def update_post(self, post_id: int, updated_post: PostBase, active_user: UserPemissions) -> Optional[Post]:
        query = select(Post).where(Post.id == post_id)
        query = self.set_scope_for_query(query=query, active_user=active_user)

        execute = await self.db.execute(query)
        post = execute.scalars().one_or_none()

        if post:
            for attr, value in updated_post.dict().items():
                if value is not None:
                    setattr(post, attr, value)
            await self.db.commit()
            await self.db.refresh(post)
        return post

    async def patch_post(self, post_id: int, patch_data: dict, active_user: UserPemissions) -> Optional[Post]:
        query = select(Post).where(Post.id == post_id)
        query = self.set_scope_for_query(query=query, active_user=active_user)

        execute = await self.db.execute(query)
        post = execute.scalars().one_or_none()

        if post:
            for attr, value in patch_data.items():
                if value is not None:
                    setattr(post, attr, value)

            await self.db.commit()
            await self.db.refresh(post)

        return post

    async def delete_post(self, post_id: int, active_user: UserPemissions) -> Optional[Post]:
        query = select(Post).where(Post.id == post_id)
        query = self.set_scope_for_query(query=query, active_user=active_user)

        if active_user.permissions["visibility"] == LOCAL_VISIBILITY_SCOPE:
            query = self.set_local_scope_for_query(
                query=query, active_user=active_user)

        execute = await self.db.execute(query)
        post = execute.scalars().one_or_none()

        if post:
            self.db.delete(post)
            await self.db.commit()

        return post

    async def get_post(self, post_id: int, active_user: UserPemissions) -> Optional[PostFull]:
        query = select(Post).where(Post.id == post_id,
                                   Post.user_id == active_user.id)
        query = self.set_scope_for_query(query=query, active_user=active_user)

        execute = await self.db.execute(query)
        post = execute.scalars().one_or_none()
        return post

    async def get_posts(
        self,
        active_user: UserPemissions,
        filters: dict = None,
        page: int = 1,
        items_per_page: int = 10,
    ) -> List[Post]:
        query = select(Post)
        query = self.set_scope_for_query(query=query, active_user=active_user)

        if filters:
            query = query.where(
                *(getattr(Post, attr) == value for attr, value in filters.items())
            )

        offset = (page - 1) * items_per_page
        query = query.offset(offset).limit(items_per_page)

        execute = await self.db.execute(query)
        posts = execute.scalars().all()
        return posts

    def set_scope_for_query(self, query, active_user: UserPemissions):
        return query.where(Post.user_id == active_user.id) if active_user.permissions["visibility"] == LOCAL_VISIBILITY_SCOPE else query


def get_post_repository(db: AsyncSession = Depends(get_async_session)) -> PostRepository:
    return PostRepository(db)
