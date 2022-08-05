from cgitb import text
from injector import inject
from dataclasses import dataclass
from sqlalchemy.orm import Session
from datetime import datetime
from twijournal.business_rules.exceptions.user_exceptions import EUsernameAlreadyExists, EUserNotExists
from twijournal.entities.post.repository import IPostRepository
from twijournal.entities.post.schema import PostCreateSchema, PostSchema, PostType
from twijournal.entities.user.repository import IUserRepository
from twijournal.entities.user.schema import UserBaseSchema, UserSchema, UserViewSchema

@inject
@dataclass
class PostUseCase():
    user_repository: IUserRepository
    post_repository: IPostRepository

    async def _insert_post(self, post: PostSchema):
        return self.post_repository.create(post)
    
    async def _create_original_post(self, user_id: int, post: PostCreateSchema) -> PostSchema:
        fullpost = PostSchema(
            post_type=PostType.ORIGINAL,
            text=post.text,
            published_by=user_id,
            published_at=datetime.now()
        )

        return await self._insert_post(fullpost)

    async def _create_reposted_post(self, user_id: int, post: PostCreateSchema):
        fullpost = PostSchema(
            reference_post_id=post.reference_post_id,
            post_type=PostType.REPOSTING,
            published_by=user_id,
            published_at=datetime.now()
        )
        return await self._insert_post(fullpost)

    async def _create_quoted_postt(self, user_id, post: PostCreateSchema):
        fullpost = PostSchema(
            reference_post_id=post.reference_post_id,
            post_type=PostType.QUOTE,
            text=post.text,
            published_by=user_id,
            published_at=datetime.now()
        )
        return await self._insert_post(fullpost)

    def _get_post_strategy(self, post_type: PostType):
        post_strategy = {
            PostType.ORIGINAL: self._create_original_post,
            PostType.REPOSTING: self._create_reposted_post,
            PostType.QUOTE: self._create_quoted_postt
        }

        return post_strategy[post_type]        

    async def create_post(self, username: str, post: PostCreateSchema):
        user = self.user_repository.get_by_username(username)
        if not user:            
            raise EUserNotExists()

        create_post = self._get_post_strategy(post.post_type)
        data = await create_post(user.id, post)

        return data
    
    async def get_posts_by_username(self, page: int, username: str):
        return self.post_repository.get_posts_by_username(page, username)
        
    async def get_posts_for_feed(self, page: int, username: str, only_following: bool):
        return self.post_repository.get_posts_for_feed(page, username, only_following)
                