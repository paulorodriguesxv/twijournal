from dataclasses import dataclass
from http import HTTPStatus
from fastapi import HTTPException, APIRouter, Depends, Response
from typing import List
from twijournal.adapters.gateway.sql_alchemy.repository.exceptions import EUserAlreadyFollowed, EUserNotFollowed, EUserNotFound
from twijournal.business_rules.exceptions.user_exceptions import EUsernameAlreadyExists
from twijournal.business_rules.use_cases.post_use_case import PostUseCase

from twijournal.business_rules.use_cases.user_use_case import UserUseCase
from twijournal.entities.followers.schema import RequestFollowSchema
from twijournal.entities.post.schema import PostPaginatedSchema
from twijournal.entities.user.schema import UserBaseSchema, UserSchema, UserViewSchema
from twijournal.adapters.endpoints.rest_fastapi.fastapi_injector import Injected, get_userid_from_token

router = APIRouter()

@router.get('/',
    summary="Get feed data",
    description="Return latests posts published by all TwiJournal users. Needs authorization header",
    response_model=PostPaginatedSchema)
async def get_feed(
    page: int = 1,
    only_following: bool = False,
    username: str = Depends(get_userid_from_token),
    post_use_case: PostUseCase = Injected(PostUseCase)):
    
    posts = await post_use_case.get_posts_for_feed(page, username, only_following)    
    return posts