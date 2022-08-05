import json
from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from twijournal.adapters.gateway.sql_alchemy.database import SqlAlchemyBase
from twijournal.adapters.gateway.sql_alchemy.models.followers import Follower


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, unique=True, index=True)
    username = Column(String(14), unique=True, index=True, nullable=False)
    email = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False)    

    
    followers = relationship(
        "User",
        secondary="followers",
        primaryjoin=Follower.followee_id==id,
        secondaryjoin=Follower.follower_id==id,
        viewonly=True)
    
    followees = relationship(
        "User",
        secondary="followers",
        primaryjoin=Follower.follower_id==id,
        secondaryjoin=Follower.followee_id==id,
        viewonly=True)    
