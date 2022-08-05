from abc import abstractmethod
from typing import List
from twijournal.entities.post.schema import PostPaginatedSchema, PostSchema
from pydantic import BaseModel

from twijournal.entities.crud_repository import ICrudRepository

class IPostRepository(ICrudRepository):
    @abstractmethod
    def create(self, post: PostSchema) -> List[BaseModel]:
        pass

    @abstractmethod
    def get_posts_by_username(self, page: int, username: str) -> PostPaginatedSchema:
        pass

    @abstractmethod
    def get_posts_for_feed(self, page: int, username: str, only_following: bool) -> PostPaginatedSchema:
        pass
