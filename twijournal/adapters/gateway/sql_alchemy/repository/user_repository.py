from injector import inject 
from dataclasses import dataclass
from typing import List
from twijournal.adapters.gateway.sql_alchemy.database import SessionDatabase
from twijournal.adapters.gateway.sql_alchemy.models.user_statistics import UserStatistics
from twijournal.adapters.gateway.sql_alchemy.repository.exceptions import EUserAlreadyFollowed, EUserNotFound
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from twijournal.adapters.gateway.sql_alchemy.models.user import User
from twijournal.adapters.gateway.sql_alchemy.repository.readwrite_repository import ReadWriteRepository
from twijournal.entities.user.repository import IUserRepository
from twijournal.entities.user.schema import UserBaseSchema, UserSchema, UserStatisticsSchema
from twijournal.entities.followers.repository import IFollowerRepository
@inject
class UserRepository(ReadWriteRepository, IUserRepository):
    
    _followers_repository: IFollowerRepository

    def __init__(self, 
        session: SessionDatabase,
        followers_repository: IFollowerRepository) -> None:
        super(UserRepository, self).__init__(session, User, UserSchema)
        self._followers_repository = followers_repository
        self.session = session

    def get_by_username(self, username: str) -> List[BaseModel]:
        with self.session.scope() as session:            
            data = session.query(self.sql_alchemy_model).filter(self.sql_alchemy_model.username==username).first()
            if data:
                return self.schema.from_orm(data)

    def _get_follow_ids(self, follower, followee):
        follower_user = self.get_by_username(follower)
        followee_user = self.get_by_username(followee)

        if (not follower_user) or (not followee_user):
            raise EUserNotFound()        
        
        return dict(
            follower_id=follower_user.id,
            followee_id=followee_user.id)

    def follow(self, follower: str, followee: str):
        follow_data = self._get_follow_ids(follower, followee)
        with self.session.scope() as session:
            try:

                followee_id = follow_data["followee_id"]
                follower_id = follow_data["follower_id"]
                self._followers_repository.follow(session, followee_id, follower_id)
                
                self.update_follower_counter(session, followee_id)
                self.update_followee_counter(session, follower_id)

                session.commit()

            except IntegrityError as error:                
                import logging
                logging.error(error)
                raise EUserAlreadyFollowed()
            except Exception as error:                
                session.rollback()
                raise error

    def _get_user_statistics(self, session, user_id):
        return session.query(UserStatistics).filter(UserStatistics.user_id==user_id).first()

    def update_follower_counter(self, session, follower_id, qty=1):
        data = self._get_user_statistics(session, follower_id)
        if data:
            data.follower_counter += qty

    def update_followee_counter(self, session, followee_id, qty=1):
        data = self._get_user_statistics(session, followee_id)
        if data:
            data.followee_counter += qty

    def update_posts_counter(self, session, user_id, qty=1):
        data = self._get_user_statistics(session, user_id)
        if data:
            data.posts_counter += qty

    def unfollow(self,  follower: str, followee: str):
        follow_data = self._get_follow_ids(follower, followee)
        with self.session.scope() as session:
            try:
                follow_increment = -1
                followee_id = follow_data["followee_id"]
                follower_id = follow_data["follower_id"]

                self._followers_repository.unfollow(session, followee_id, follower_id)
                self.update_follower_counter(session, followee_id, follow_increment)
                self.update_followee_counter(session, follower_id, follow_increment)

                session.commit()            
            except Exception as error:                
                session.rollback()
                raise error

    def get_statistics(self, user_id: int) -> BaseModel:
        with self.session.scope() as session:        
            data = self._get_user_statistics(session, user_id)
            return UserStatisticsSchema.from_orm(data)

    def create(self, user: UserBaseSchema) -> BaseModel:
        with self.session.scope() as session:
            db_data = self.sql_alchemy_model(**user.dict())    
            session.add(db_data)
            
            session.commit()
            # refresh ids
            db_data = session.query(self.sql_alchemy_model).filter(self.sql_alchemy_model.username==user.username).first()
            
            user_statatistics = UserStatistics(
                        user_id=db_data.id,
                        followee_counter=0,
                        follower_counter=0,
                        posts_counter=0
                    )
            session.add(user_statatistics)            
            session.commit()
            
            db_data = session.query(self.sql_alchemy_model).filter(self.sql_alchemy_model.username==user.username).first()
            return self.schema.from_orm(db_data)            