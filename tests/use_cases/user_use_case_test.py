from contextlib import contextmanager
from http import HTTPStatus
from twijournal.adapters.endpoints import rest_fastapi
from twijournal.adapters.gateway.sql_alchemy.database import SessionDatabase, SessionLocal, SqlAlchemyBase
from twijournal.adapters.gateway.sql_alchemy.repository.follower_respository import FollowerRepository
from twijournal.adapters.gateway.sql_alchemy.repository.user_repository import UserRepository
from twijournal.business_rules.use_cases.user_use_case import UserUseCase
from twijournal.entities.followers.repository import IFollowerRepository
from twijournal.entities.user.repository import IUserRepository
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from injector import Injector
from pydantic import ValidationError


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestSessionDatabase():
        
    @staticmethod
    @contextmanager
    def scope():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

@pytest.fixture()
def users():
    return [
        {
            "id": 0,
            "username": "gF3tSy6ARGrCD",
            "created_at": "2022-04-19T15:31:08.581Z"
        },
        {
            "id": 1,
            "username": "gF4tSy6ARGrCD",
            "created_at": "2022-04-19T15:31:08.581Z"
        },
        {
            "id": 2,
            "username": "gF5tSy6ARGrCD",
            "created_at": "2022-04-19T15:31:08.581Z"
        }                     
    ]

@pytest.fixture()
def main_user_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwidXNlcm5hbWUiOiJnRjN0U3k2QVJHckNEIiwiaWF0IjoxNTE2MjM5MDIyfQ.mR0ljmSEjkV0bLUluYx24pfOANQ4vBuSU71MluSokr0"

@pytest.fixture()
def test_db():
    SqlAlchemyBase.metadata.create_all(bind=engine)
    yield
    SqlAlchemyBase.metadata.drop_all(bind=engine)

def configure(binder):
  
    # database
    binder.bind(SessionDatabase, to=TestSessionDatabase)

    # repositories
    binder.bind(IUserRepository, to=UserRepository)
    binder.bind(IFollowerRepository, to=FollowerRepository)

    #use cases
    binder.bind(UserUseCase, to=UserUseCase)

injector = Injector([configure])
app = rest_fastapi.build(injector=injector)

client = TestClient(app)

def test_new_user_is_created(test_db, users):
    """
    - Only alphanumeric characters can be used for username
    - Maximum 14 characters for username
    """
    payload = users[0]
    response = client.post('/users/', json=payload)

    assert response.status_code == HTTPStatus.CREATED

def test_should_fail_when_new_user_have_more_than_14_char(test_db, users):
    """
    - Only alphanumeric characters can be used for username
    - Maximum 14 characters for username
    """
    payload =  {
            "id": 0,
            "username": "gF3tSy6Aasdadadas",
            "created_at": "2022-04-19T15:31:08.581Z"
        }


    response = client.post('/users/', json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "ensure this value has at most 14 characters" in response.json()["detail"][0]["msg"]


def test_should_fail_when_try_follow_someone_without_jwt(test_db, users):
    """Users should be able to follow other users"""
    payload = users[0]
    client.post('/users/', json=payload)    

    payload = {
    "followee": "gF4tSy6ARGrCD"
    }
    response = client.post('/users/follow', json=payload)
    assert response.status_code == HTTPStatus.IM_A_TEAPOT    
    

def test_should_have_one_follower_when_followed_by_someone(test_db, main_user_token, users):
    """Users should be able to follow other users"""

    payload = users[0]
    response = client.post('/users/', json=payload)

    payload = users[1]
    client.post('/users/', json=payload)   

    payload = {
        "followee": users[1]["username"]
    }
    response = client.post('/users/follow', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})
    assert response.status_code == HTTPStatus.CREATED


    response = client.get(f'/users/{users[0]["username"]}')   

    assert response.json()["user"]["followees"][0]["username"] == users[1]["username"]

def test_should_have_one_followee_when_follow_someone(test_db, main_user_token, users):
    """Users should be able to follow other users"""

    payload = users[0]
    response = client.post('/users/', json=payload)

    payload = users[1]
    client.post('/users/', json=payload)   

    payload = {
    "followee": users[1]["username"]
    }
    response = client.post('/users/follow', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})
    assert response.status_code == HTTPStatus.CREATED

    response = client.get(f'/users/{users[1]["username"]}')   

    assert response.json()["user"]["followers"][0]["username"] == users[0]["username"]

def test_should_have_zero_followee_when_unfollow_someone(test_db, main_user_token, users):
    """Users should be able to follow other users"""

    payload = users[0]
    response = client.post('/users/', json=payload)

    payload = users[1]
    client.post('/users/', json=payload)   

    payload = {
    "followee": users[1]["username"]
    }
    response = client.post('/users/follow', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})
    assert response.status_code == HTTPStatus.CREATED
    
    response = client.get(f'/users/{users[1]["username"]}')   
    assert len(response.json()["user"]["followers"]) == 1

    response = client.delete('/users/follow', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(f'/users/{users[1]["username"]}')   

    assert len(response.json()["user"]["followers"]) == 0   


def test_should_fail_on_try_following_himself(test_db, main_user_token, users):
    """Users cannot follow themselves"""

    payload = users[0]
    response = client.post('/users/', json=payload)

    payload = users[1]
    client.post('/users/', json=payload)   

    payload = {
    "followee": users[0]["username"]
    }

    with pytest.raises(ValidationError) as execinfo:
        response = client.post('/users/follow', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})
    
    assert "user can't follow himself" in str(execinfo.value)
    
def test_should_have_followee_equal_two_when_follow_two_person(test_db, main_user_token, users):
    """Users should be able to follow other users"""

    payload = users[0]
    client.post('/users/', json=payload)

    payload = users[1]    
    client.post('/users/', json=payload)   

    payload = users[2]
    client.post('/users/', json=payload)   

    payload = {
        "followee": users[1]["username"]
    }
    print(payload)
    response = client.post('/users/follow', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})

    payload = {
        "followee": users[2]["username"]
    }
    print(payload)
    response = client.post('/users/follow', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})

    response = client.get(f'/users/{users[0]["username"]}')   

    
    assert response.json()["statistics"]["followee_counter"] == 2