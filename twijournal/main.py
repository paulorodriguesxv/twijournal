from injector import Injector
from sqlalchemy.orm import Session
from migrations.migration_helper import execute_migration


from twijournal.adapters.gateway.sql_alchemy.database import SessionDatabase
from twijournal.adapters.gateway.sql_alchemy.repository.follower_respository import FollowerRepository
from twijournal.adapters.gateway.sql_alchemy.repository.post_repository import PostRepository
from twijournal.adapters.gateway.sql_alchemy.repository.user_repository import UserRepository
from twijournal.business_rules.use_cases.post_use_case import PostUseCase

from twijournal.business_rules.use_cases.user_use_case import UserUseCase
from twijournal.entities.followers.repository import IFollowerRepository
from twijournal.entities.post.repository import IPostRepository

from twijournal.entities.user.repository import IUserRepository

# for fast api
from twijournal.adapters.endpoints import rest_fastapi
from twijournal.infrastructure.config import DefaultConfig

def configure(binder):
  
    # database
    binder.bind(SessionDatabase, to=SessionDatabase)

    # repositories
    binder.bind(IUserRepository, to=UserRepository)
    binder.bind(IFollowerRepository, to=FollowerRepository)
    binder.bind(IPostRepository, to=PostRepository)
    
    #use cases
    binder.bind(UserUseCase, to=UserUseCase)
    binder.bind(PostUseCase, to=PostUseCase)

injector = Injector([configure])
app = rest_fastapi.build(injector=injector)


@app.on_event("startup")
async def startup_event():
    execute_migration()
