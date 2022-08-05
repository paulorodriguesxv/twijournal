from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey, Table, UniqueConstraint

from twijournal.adapters.gateway.sql_alchemy.database import SqlAlchemyBase



class Follower(SqlAlchemyBase):
    __tablename__ = "followers"

    followee_id = Column(BigInteger, ForeignKey('users.id'), index=True, nullable=False, primary_key=True)
    follower_id = Column(BigInteger, ForeignKey('users.id'), index=True, nullable=False, primary_key=True)    
    created_at = Column(DateTime, nullable=False)    

    UniqueConstraint('followee_id', 'follower_id', name='unique_follower')    