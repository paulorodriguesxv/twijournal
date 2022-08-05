from dataclasses import dataclass
from http import HTTPStatus
from fastapi import HTTPException, APIRouter, Depends, Response
from typing import List
from twijournal.adapters.gateway.sql_alchemy.repository.exceptions import EUserAlreadyFollowed, EUserNotFollowed, EUserNotFound
from twijournal.business_rules.exceptions.user_exceptions import EUsernameAlreadyExists

from twijournal.business_rules.use_cases.user_use_case import UserUseCase
from twijournal.entities.followers.schema import RequestFollowSchema
from twijournal.entities.user.schema import UserBaseSchema, UserSchema, UserViewSchema
from twijournal.adapters.endpoints.rest_fastapi.fastapi_injector import Injected, get_userid_from_token

router = APIRouter()

@router.get("/",
    summary="Get all users profiles sumamarized data from the system",
    description="Return user data. I.E: name, email, id, followers, followees",
    response_model=List[UserSchema])
async def users(user_use_case: UserUseCase = Injected(UserUseCase)):
    user_c = await user_use_case.get_all()    
    return user_c

@router.get(
    "/{username}", 
    summary="Get user profile data from a specific user",
    description="Return user data. I.E: name, followers, followees, counters, etc.",
    responses={
        200: {
            "model": UserViewSchema,
            "description": "Return user data. I.E: name, followers, followees, counters, etc."
        },
        404: {"description": "When user not found"},
    })
async def users(
    username: str,
    user_use_case: UserUseCase = Injected(UserUseCase)):
    user_c = await user_use_case.get_user_for_view(username)    
    if not user_c:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
        
    return user_c


@router.post("/",
    summary="Register a new user",
    description="Use this endpoint when you want to register a new user",  
    response_model=UserSchema,
    status_code=HTTPStatus.CREATED)
async def users(user: UserBaseSchema, user_use_case: UserUseCase = Injected(UserUseCase)):
    try:
        user_c = await user_use_case.register_user(user)
    except EUsernameAlreadyExists:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User already exists")
    
    return user_c    

@router.post(
    "/follow",    
    summary="Follow user",
    description="Use this endpoint when you want to follow an user. Needs authorization header",   
    status_code=201,
    responses={
        201: {"description": "User created", "content": None},
        404: {"description": "When user not found"},
        409: {"description": "When user already exists"},
        418: {"description": "Missing Authorization header"}        
        })
async def users(
    request: RequestFollowSchema, 
    username: str = Depends(get_userid_from_token),    
    user_use_case: UserUseCase = Injected(UserUseCase)):

    try:
        await user_use_case.follow_user(username, request.followee)    
    except EUserAlreadyFollowed: 
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="User already followed")    
    except EUserNotFound: 
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")            


    return Response(status_code=HTTPStatus.CREATED)


@router.delete("/follow", 
    summary="Unfollow user",
    description="Use this endpoint when you want to unfollow an user. Needs authorization header",   
    status_code=204,
    responses={
        204: {"description": "User created", "content": None},
        404: {"description": "When user not found"},
        418: {"description": "Missing Authorization header"}})
async def users(
    request: RequestFollowSchema, 
    username: str = Depends(get_userid_from_token),    
    user_use_case: UserUseCase = Injected(UserUseCase)):

    try:
        await user_use_case.unfollow_user(username, request.followee)    
    except (EUserNotFollowed, EUserNotFound): 
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not followed")    


    return Response(status_code=HTTPStatus.NO_CONTENT)