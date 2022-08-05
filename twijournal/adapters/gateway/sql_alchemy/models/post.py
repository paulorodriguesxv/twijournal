from email.policy import default
from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from twijournal.adapters.gateway.sql_alchemy.database import SqlAlchemyBase
from twijournal.adapters.gateway.sql_alchemy.models.followers import Follower

from sqlalchemy.orm import backref

class Post(SqlAlchemyBase):
    __tablename__ = "posts"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, unique=True, index=True)
    reference_post_id = Column(BigInteger, ForeignKey("posts.id"), index=True, nullable=True)
    post_type = Column(String(10), nullable=False)
    text = Column(String(777), nullable=True)
    published_by = Column(BigInteger, ForeignKey("users.id"), index=True, nullable=False)
    published_at = Column(DateTime, nullable=False)   

    publisher = relationship("User", viewonly=True) 
    reference_post = relationship("Post", backref=backref("posts", uselist=False), remote_side=[id],  viewonly=True) 
