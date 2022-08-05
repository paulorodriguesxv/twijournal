from enum import Enum
from twijournal.entities.user.schema import UserBaseSchema, UserSchema
from pydantic import BaseModel, validator, constr
from typing import Optional, List
from datetime import datetime

class PostType(str, Enum):
    ORIGINAL = "original"
    REPOSTING = "reposting"
    QUOTE = "quote"
    
class _PostSchema(BaseModel):
    id: Optional[int]
    reference_post_id: Optional[int]
    post_type: PostType
    text: Optional[constr(max_length=777)]
    published_by: int
    published_at: datetime
    
    class Config:
        orm_mode = True  

class PostSchema(_PostSchema):   
    id: Optional[int]
    reference_post_id: Optional[int]
    post_type: PostType
    text: Optional[constr(max_length=777)]
    published_by: int
    published_at: datetime

    publisher: Optional[UserBaseSchema]
    reference_post: Optional["PostSchema"]

    class Config:
        orm_mode = True

class PostCreateSchema(BaseModel):
    reference_post_id: Optional[int]
    post_type: PostType
    text: Optional[constr(max_length=777)]     

class HateoasSchema(BaseModel):
    rel: str
    href: Optional[str]

class PostSchemaHateoasSchema(BaseModel):
    post: PostSchema
    following_user: bool = False
    links: Optional[List[HateoasSchema]]

class PostPaginatedSchema(BaseModel):
    posts: List[PostSchemaHateoasSchema]
    page_number: int
    total_pages: int
    total_posts: int
    links: Optional[List[HateoasSchema]]

class PostStatisticsSchema(BaseModel):
    id: int
    user_id: int
    year: int
    year_day: int
    post_counter: int
