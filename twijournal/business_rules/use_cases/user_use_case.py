from injector import inject
from dataclasses import dataclass
from sqlalchemy.orm import Session
from datetime import datetime
from twijournal.business_rules.exceptions.user_exceptions import EUsernameAlreadyExists, EUserNotExists
from twijournal.entities.user.repository import IUserRepository
from twijournal.entities.user.schema import UserBaseSchema, UserSchema, UserViewSchema

@inject
@dataclass
class UserUseCase():
    user_repository: IUserRepository

    async def register_user(self, user: UserBaseSchema):
        user_found = self.user_repository.get_by_username(user.username)
        if user_found:
            raise EUsernameAlreadyExists()
        return self.user_repository.create(user)
    
    async def get_by_username(self, username: str):
        return self.user_repository.get_by_username(username)

    async def get_all(self):
        return self.user_repository.get_all()

    async def follow_user(self, follower: str, followee: str):
        return self.user_repository.follow(follower, followee)

    async def unfollow_user(self, follower, followee):
        return self.user_repository.unfollow(follower, followee)

    async def get_user_for_view(self, username: str):
        user = await self.get_by_username(username)
        if not user:
            raise EUserNotExists()        

        user_statistics = self.user_repository.get_statistics(user.id)             
        return UserViewSchema(
            statistics=user_statistics,
            user=user
        )        