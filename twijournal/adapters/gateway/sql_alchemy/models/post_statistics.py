from email.policy import default
from sqlalchemy import Column, String, BigInteger, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from twijournal.adapters.gateway.sql_alchemy.database import SqlAlchemyBase


class PostStatistics(SqlAlchemyBase):
    __tablename__ = "posts_statistics"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    user_id = Column(BigInteger,  ForeignKey('users.id'), nullable=False)
    year = Column(Integer, nullable=False)
    year_day = Column(Integer, nullable=False)
    post_counter = Column(BigInteger, nullable=False, default=0)
    
    UniqueConstraint('user_id', 'year', 'year_day', name='unique_entry_by_user')
    