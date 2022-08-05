from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, #connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SqlAlchemyBase = declarative_base()


class SessionDatabase():
        
    @staticmethod
    @contextmanager
    def scope():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
