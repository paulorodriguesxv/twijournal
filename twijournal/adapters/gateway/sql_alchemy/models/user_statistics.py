from email.policy import default
from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from twijournal.adapters.gateway.sql_alchemy.database import SqlAlchemyBase


class UserStatistics(SqlAlchemyBase):
    __tablename__ = "users_statistics"

    id = Column('id', BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    user_id = Column('user_id', BigInteger,  ForeignKey('users.id'), nullable=False, unique=True)
    followee_counter = Column('followee_counter', BigInteger, nullable=False, default=0)
    follower_counter = Column('follower_counter', BigInteger, nullable=False, default=0)
    posts_counter = Column('posts_counter', BigInteger, nullable=False, default=0)
