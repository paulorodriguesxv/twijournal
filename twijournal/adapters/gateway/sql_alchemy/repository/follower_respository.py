from injector import inject 
from datetime import datetime
from twijournal.adapters.gateway.sql_alchemy.database import SessionDatabase
from twijournal.adapters.gateway.sql_alchemy.repository.exceptions import EUserNotFollowed
from pydantic import BaseModel
from sqlalchemy.orm import Session

from twijournal.adapters.gateway.sql_alchemy.models.followers import Follower
from twijournal.adapters.gateway.sql_alchemy.repository.readwrite_repository import ReadWriteRepository
from twijournal.entities.followers.schema import FollowerSchema
from twijournal.entities.followers.repository import IFollowerRepository

@inject
class FollowerRepository(ReadWriteRepository, IFollowerRepository):

    def __init__(self, session: SessionDatabase) -> None:
        super(FollowerRepository, self).__init__(session, Follower, FollowerSchema)

    def follow(self, session: Session, followee_id: int, follower_id: int) -> BaseModel:
        follower = FollowerSchema(
            followee_id=followee_id,
            follower_id=follower_id,
            created_at= datetime.now()
        )

        db_data = self.sql_alchemy_model(**follower.dict())    
        session.add(db_data)

        return self.schema.from_orm(db_data)


    def unfollow(self, session: Session, followee_id: int, follower_id: int):
        follower = session.query(self.sql_alchemy_model).filter(self.sql_alchemy_model.followee_id==followee_id,
            self.sql_alchemy_model.follower_id==follower_id)
        if not follower.first():
            raise EUserNotFollowed()

        follower.delete()