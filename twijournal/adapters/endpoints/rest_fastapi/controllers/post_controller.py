from dataclasses import dataclass
from http import HTTPStatus
from fastapi import HTTPException, APIRouter, Depends, Response
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from twijournal.adapters.gateway.sql_alchemy.repository.exceptions import EMaxUserPostPerDay, EUserAlreadyFollowed, EUserNotFollowed, EUserNotFound
from twijournal.business_rules.exceptions.user_exceptions import EUsernameAlreadyExists
from twijournal.business_rules.use_cases.post_use_case import PostUseCase

from twijournal.business_rules.use_cases.user_use_case import UserUseCase
from twijournal.entities.followers.schema import RequestFollowSchema
from twijournal.entities.post.schema import PostCreateSchema, PostPaginatedSchema, PostSchema
from twijournal.entities.user.schema import UserBaseSchema, UserSchema, UserViewSchema
from twijournal.adapters.endpoints.rest_fastapi.fastapi_injector import Injected, get_userid_from_token
from twijournal.infrastructure.config import DefaultConfig


router = APIRouter()

@router.post("/", 
    summary="Create a new post",
    description="Allows user to create post, reposting or quote a existing post. Need pass Authorization Header.",
    status_code=201,
    responses={
        201: {"model": PostSchema, "description": "Return created post"},
        403: {"description": "When user exceed your daily post quota"},
        404: {"description": "When user not found"},
        418: {"description": "Missing Authorization header"}        
        })
async def create_post(
    post: PostCreateSchema,
    username: str = Depends(get_userid_from_token),
    post_use_case: PostUseCase = Injected(PostUseCase)):

    try:
        _post = await post_use_case.create_post(username, post)    
    except EMaxUserPostPerDay:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=f"Daily user quote of {DefaultConfig.USER_MAX_POST_PER_DAY} post reached.")

    return JSONResponse(status_code=HTTPStatus.CREATED, content=jsonable_encoder(_post))


@router.get('/{username}',
    summary="Get post created for a given user",
    description="Return all paginated data post from user",
    response_model=PostPaginatedSchema)
async def get_posts_by_username(
    username: str,
    page: int,
    post_use_case: PostUseCase = Injected(PostUseCase)):
    posts = await post_use_case.get_posts_by_username(page, username)    
    return posts