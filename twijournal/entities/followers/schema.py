from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class FollowerSchema(BaseModel):
    followee_id: int
    follower_id: int
    created_at: datetime


    @validator("follower_id")
    def must_not_to_be_himself(cls, v, values, **kwargs):
        if ("followee_id" in values) and (v == values["followee_id"]):
            raise ValueError("user can't follow himself")
        return v

    class Config:
        orm_mode = True


class RequestFollowSchema(BaseModel):
    followee: Optional[str]
