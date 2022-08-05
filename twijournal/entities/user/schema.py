from pydantic import BaseModel, validator, constr
from typing import Optional, List
from datetime import datetime

def get_uuid():
    return uuid4().hex


class UserBaseSchema(BaseModel):
    id: int = ...
    username: constr(max_length=14, regex='^[a-zA-Z0-9]+$') = ...
    email: Optional[str]
    name: Optional[str] = None
    created_at: datetime = ...

    class Config:
        orm_mode = True

class UserSchema(UserBaseSchema):
    followers: Optional[List[UserBaseSchema]]
    followees: Optional[List[UserBaseSchema]]

    class Config:
        orm_mode = True

class UserStatisticsSchema(BaseModel):
    followee_counter: int = 0
    follower_counter: int = 0
    posts_counter: int = 0

    class Config:
        orm_mode = True

class UserViewSchema(BaseModel):
    user: UserSchema
    statistics: UserStatisticsSchema

class TokenUserSchema(BaseModel):
    username: str