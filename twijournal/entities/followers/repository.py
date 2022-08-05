from abc import abstractmethod
from typing import List
from pydantic import BaseModel

from twijournal.entities.crud_repository import ICrudRepository

class IFollowerRepository(ICrudRepository):
    @abstractmethod
    def follow(self, session, followee_id:  int, follower_id: int) -> List[BaseModel]:
        pass

    @abstractmethod
    def unfollow(self, session, followee_id:  int, follower_id: int):
        pass
