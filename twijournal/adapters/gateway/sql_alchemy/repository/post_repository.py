from datetime import datetime
import statistics
from injector import inject 
from typing import List
from pydantic import BaseModel
from twijournal.adapters.gateway.sql_alchemy.models.post_statistics import PostStatistics
from twijournal.adapters.gateway.sql_alchemy.repository.follower_respository import FollowerRepository
from twijournal.entities.user.schema import UserBaseSchema, UserSchema
from twijournal.infrastructure.config import DefaultConfig
from twijournal.adapters.gateway.sql_alchemy.database import SessionDatabase
from twijournal.adapters.gateway.sql_alchemy.models.post import Post
from twijournal.adapters.gateway.sql_alchemy.repository.exceptions import EMaxUserPostPerDay, EUserNotFound
from twijournal.adapters.gateway.sql_alchemy.repository.pagination import paginate
from twijournal.adapters.gateway.sql_alchemy.repository.readwrite_repository import ReadWriteRepository
from twijournal.entities.post.repository import IPostRepository
from twijournal.entities.post.schema import HateoasSchema, PostPaginatedSchema, PostSchema, PostSchemaHateoasSchema
from twijournal.entities.user.repository import IUserRepository
from twijournal.adapters.gateway.sql_alchemy.models.followers import Follower

NEXT_PAGE_REL_LABEL = "next_page"
PREVIOUS_POST_REL_LABEL = "previous_page"
POST_REL_LABEL = "post"

@inject
class PostRepository(ReadWriteRepository, IPostRepository):
    
    user_repository: IUserRepository

    def __init__(self, 
        session: SessionDatabase,
        user_repository: IUserRepository) -> None:
        super(PostRepository, self).__init__(session, Post, PostSchema)
        self.session = session
        self.user_repository = user_repository

    def _build_hateos_for_post(self, post: PostSchema):
        hateoas = HateoasSchema(
            rel=POST_REL_LABEL,
            href=f"{DefaultConfig.POST_URI}{post.id}"
        )
        return PostSchemaHateoasSchema(post=post, links=[hateoas])


    def get_posts_by_username(self, page: int, username: str) -> PostPaginatedSchema:
        with self.session.scope() as session:            
            user = self.user_repository.get_by_username(username)
            if not user:
                raise EUserNotFound()

            posts_query = session.query(
                self.sql_alchemy_model).\
                    filter(self.sql_alchemy_model.published_by==user.id).\
                    order_by(self.sql_alchemy_model.id.desc())
            data = paginate(posts_query, page, DefaultConfig.MAX_POSTS_PER_PAGE)
            if not data:
                return
            
            return self._build_response_hateoas(page, self._build_resource_uri_for_posts(username), data)

    def get_posts_for_feed(self, page: int, username: str, only_following: bool) -> PostPaginatedSchema:
        user: UserSchema = self.user_repository.get_by_username(username)
        followees = [user.id for user in user.followees] if user else []

        followers_criteria = True
        with self.session.scope() as session:            
            if only_following:
                followers_criteria = session.query(Follower).\
                    filter(Follower.follower_id==user.id,
                    Follower.followee_id==self.sql_alchemy_model.published_by).\
                    exists()

            posts_query = session.query(
                self.sql_alchemy_model).\
                    filter(followers_criteria).\
                    order_by(self.sql_alchemy_model.id.desc())
            data = paginate(posts_query, page, DefaultConfig.MAX_FEED_POSTS_PER_PAGE)
            if not data:
                return
            
            pagination_extra_filter = ""
            if only_following:
                pagination_extra_filter = f"&only_following={only_following}"
            data = self._build_response_hateoas(page, self._build_resource_uri_for_feed(), data, pagination_extra_filter)
                
            for item in data.posts:
                item.following_user = item.post.published_by in followees

            return data

    def _build_resource_uri_for_posts(self, username: str):
        return f"{DefaultConfig.POST_URI}{username}"

    def _build_resource_uri_for_feed(self):
        return f"{DefaultConfig.FEED_URI}"        

    def _build_response_hateoas(self, page, resource_uri, data, extra_filter=None):
        posts = list(map(self.schema.from_orm, data.items))
        
        next_page = HateoasSchema(
                rel=NEXT_PAGE_REL_LABEL,
                href=f"{resource_uri}?page={data.next_page}{extra_filter}" if data.has_next else None
            )

        previous_page = HateoasSchema(
                rel=PREVIOUS_POST_REL_LABEL,
                href= f"{resource_uri}?page={data.previous_page}{extra_filter}" if data.has_previous else None
            )

        return PostPaginatedSchema(
                posts=list(map(self._build_hateos_for_post, posts)),
                page_number=page,
                total_posts=data.total,
                total_pages=data.pages,
                links=[previous_page, next_page]
            )

    def _get_year_and_day(self, date: datetime):
        year = date.year
        year_day = date.timetuple().tm_yday        

        return year, year_day

    def _get_post_statistics(self, session, user_id):
        year, year_day = self._get_year_and_day(datetime.now())
        
        statistics = session.query(PostStatistics).\
                    filter(
                        PostStatistics.user_id==user_id,
                        PostStatistics.year==year,
                        PostStatistics.year_day==year_day).first()

        return statistics

    def _update_post_statistics(self, session, post: PostSchema, statistics: PostStatistics):
        if statistics:
            statistics.post_counter += 1
        else:
            year, year_day = self._get_year_and_day(datetime.now())        
            statistics = PostStatistics(
                user_id=post.published_by,
                year=year,
                year_day=year_day,
                post_counter=1
            )
            session.add(statistics)

    def _validate_user_is_able_to_create_post(self, statistics: PostStatistics):
        if not statistics: 
            return

        if statistics.post_counter >= DefaultConfig.USER_MAX_POST_PER_DAY:
            raise EMaxUserPostPerDay()

    def create(self, post: PostSchema) -> List[BaseModel]:
        with self.session.scope() as session:  

            statistics = self._get_post_statistics(session, post.published_by)
            self._validate_user_is_able_to_create_post(statistics)

            db_data = self.sql_alchemy_model(**post.dict())    
            session.add(db_data)            
            
            self._update_post_statistics(session, post, statistics)
            self.user_repository.update_posts_counter(session, db_data.published_by)

            session.commit()            
            session.refresh(db_data)
            #db_data = session.query(self.sql_alchemy_model).filter(self.sql_alchemy_model.username==model.username).first()
            return self.schema.from_orm(db_data)