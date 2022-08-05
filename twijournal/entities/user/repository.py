from abc import abstractmethod
from typing import List
from pydantic import BaseModel

from twijournal.entities.crud_repository import ICrudRepository
from twijournal.entities.user.schema import UserBaseSchema

class IUserRepository(ICrudRepository):
    @abstractmethod
    def get_by_username(self, username: str) -> List[BaseModel]:
        pass

    @abstractmethod
    def follow(self, follower: str, followee: str) -> BaseModel:
        pass

    @abstractmethod
    def unfollow(self, follower: str, followee: str) -> BaseModel:
        pass

    @abstractmethod
    def get_statistics(self, user_id: int) -> BaseModel:
        pass

    @abstractmethod
    def create(self, user: UserBaseSchema) -> BaseModel:
        pass       

    @abstractmethod
    def update_follower_counter(self, session, follower_id, qty=1):
        pass

    @abstractmethod
    def update_followee_counter(self, session, followee_id, qty=1):
        pass

    @abstractmethod
    def update_posts_counter(self, session, user_id, qty=1):
        pass