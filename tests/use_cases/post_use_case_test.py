from contextlib import contextmanager
from http import HTTPStatus
from twijournal.adapters.endpoints import rest_fastapi
from twijournal.adapters.gateway.sql_alchemy.database import SessionDatabase, SessionLocal, SqlAlchemyBase
from twijournal.adapters.gateway.sql_alchemy.repository.follower_respository import FollowerRepository
from twijournal.adapters.gateway.sql_alchemy.repository.post_repository import PostRepository
from twijournal.adapters.gateway.sql_alchemy.repository.user_repository import UserRepository
from twijournal.business_rules.use_cases.post_use_case import PostUseCase
from twijournal.business_rules.use_cases.user_use_case import UserUseCase
from twijournal.entities.followers.repository import IFollowerRepository
from twijournal.entities.post.repository import IPostRepository
from twijournal.entities.user.repository import IUserRepository
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from injector import Injector
from pydantic import ValidationError
from twijournal.infrastructure.config import DefaultConfig
from twijournal.infrastructure.jwt_generator import generate_jwt

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DefaultConfig.USER_MAX_POST_PER_DAY = 5

class TestSessionDatabase():
        
    @staticmethod
    @contextmanager
    def scope():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

users_list = [
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
def users():
    return users_list

@pytest.fixture()
def main_user_token():
    return generate_jwt(users_list[0]["username"])

@pytest.fixture(scope='module', autouse=True)
def setup():
    SqlAlchemyBase.metadata.create_all(bind=engine)
    yield
    SqlAlchemyBase.metadata.drop_all(bind=engine)

def configure(binder):
  
    # database
    binder.bind(SessionDatabase, to=TestSessionDatabase)

    # repositories
    binder.bind(IUserRepository, to=UserRepository)
    binder.bind(IFollowerRepository, to=FollowerRepository)
    binder.bind(IPostRepository, to=PostRepository)

    #use cases
    binder.bind(UserUseCase, to=UserUseCase)
    binder.bind(PostUseCase, to=PostUseCase)



injector = Injector([configure])
app = rest_fastapi.build(injector=injector)

client = TestClient(app)

def configure_create_users(users):
    for user in users:
        client.post('/users/', json=user)

def configure_follow_users(users, main_user_token):
    payload = {
        "followee": users[2]["username"]
    }
    client.post('/users/follow', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})
     

def test_start_user_configuration(users, main_user_token):
    configure_create_users(users)
    configure_follow_users(users, main_user_token)
    response = client.get(f'/users/{users[0]["username"]}')   
    assert response.status_code==HTTPStatus.OK

def test_should_be_able_to_post_original_successfully(users, main_user_token):
    payload = {
        "post_type": "original",
        "text": "My test original post"
    }    
    response = client.post('/posts/', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})  
    assert response.status_code==HTTPStatus.CREATED

    response = client.get(f'/posts/{users[0]["username"]}?page=1')   
    assert response.status_code==HTTPStatus.OK

    json_response =response.json()
    assert json_response["page_number"] == 1
    assert json_response["total_pages"] == 1
    assert json_response["total_posts"] == 1
    assert json_response["links"][0]["rel"] == "previous_page"
    assert json_response["links"][1]["rel"] == "next_page"

def test_should_be_able_to_repost_successfully(users, main_user_token):
    payload = {
        "post_type": "reposting",
        "reference_post_id": 1,
    }    
    response = client.post('/posts/', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})  
    assert response.status_code==HTTPStatus.CREATED

    response = client.get(f'/posts/{users[0]["username"]}?page=1')   
    assert response.status_code==HTTPStatus.OK    

    json_response =response.json()
    assert json_response["posts"][0]["post"]["reference_post_id"] == 1
    assert json_response["posts"][0]["post"]["post_type"] == "reposting"
    assert json_response["posts"][0]["post"]["reference_post"]["post_type"] == "original"

def test_should_be_able_to_quote_post_successfully(users, main_user_token):
    payload = {
        "post_type": "quote",
        "text": "Don't believe on this post",
        "reference_post_id": 1,
    }    
    response = client.post('/posts/', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})  
    assert response.status_code==HTTPStatus.CREATED

    response = client.get(f'/posts/{users[0]["username"]}?page=1')   
    assert response.status_code==HTTPStatus.OK    

    json_response =response.json()
    assert json_response["posts"][0]["post"]["reference_post_id"] == 1
    assert json_response["posts"][0]["post"]["text"] == "Don't believe on this post"
    assert json_response["posts"][0]["post"]["post_type"] == "quote"
    assert json_response["posts"][0]["post"]["reference_post"]["post_type"] == "original"    

def test_should_allow_max_size_text_successfully(users, main_user_token):
    payload = {
        "post_type": "original",
        "text": "3cokqxzlNhIFOUbwvO3ggu6V7eG8mEtPIWwBy4PslzHreblD4ef8GWKwQBKT43yjYo9rSLhyC0b40o5TYqBodFOpykqm9oa762MoCUHNvGdvMSBWAMS9AlLskSqZ2qu6zRC3OigCI1WTJAMv1wXjaTIh6fBrbbgFdNcYjHW9x0FSUvrwJbo9hLN4X8XPD091IudCu2Zc2AT5l0AhJ6SRY0esD2uKEFWbZYs8OzXdzGmHYzphaUWk6m4k2dwBkcKH1Noh9pGXPQyjzQYBCfdpCG7nhGPn9O35dVIfiWrSxvHqhebjB4J5kXjxDZ8yLwGF6O0a184KxPPTP81vIer2YHZ2YCAzbSD2T0LrJO1OrMo3DGZH4H2lDoAq9317LykWxZ7OK1OVe2fQAx6Dv0ELZBt27BwmBoHdJ4V3zzG3SH3ycDaYBVKL2yYKbpIiE7JhlNWnL83ZDs3zgSaeGvfe6jjvyxJlyYkzUlQQZhXmUZp8OP9AIAK2qNV1QpuUPB03WZv94KYJc9M17z4WcfvJE0YOp3aejMXix6awWAdpvPC5E4A4Z6SmHYW8IxZXm0CJVu7oRLE91QxENX2LvtIsTMNoMzLuZQndLH31XeX7BvvPBtI0QlRZ3kJwnuMO0BoILxaceGuNM32Q5JKkcgnz1Yq8pYvytpvaSD2CIacuNUxQG3g5JrsUOTAC34vogfJX6kFZQogIDSBXKEUfBye70dFXGgi8eDsLEzVdzEL3aFNQ5w0MtN1XWke5GT25poQC3laqSHOG8"

    }    
    response = client.post('/posts/', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})  
    assert response.status_code==HTTPStatus.CREATED    

def test_should_fail_when_max_size_text_overcome(users, main_user_token):
    payload = {
        "post_type": "original",
        "text": "3cokqxzlNhIFasdfasdfOUbwvO3ggu6V7eG8mEtPIWwBy4PslzHreblD4ef8GWKwQBKT43yjYo9rSLhyC0b40o5TYqBodFOpykqm9oa762MoCUHNvGdvMSBWAMS9AlLskSqZ2qu6zRC3OigCI1WTJAMv1wXjaTIh6fBrbbgFdNcYjHW9x0FSUvrwJbo9hLN4X8XPD091IudCu2Zc2AT5l0AhJ6SRY0esD2uKEFWbZYs8OzXdzGmHYzphaUWk6m4k2dwBkcKH1Noh9pGXPQyjzQYBCfdpCG7nhGPn9O35dVIfiWrSxvHqhebjB4J5kXjxDZ8yLwGF6O0a184KxPPTP81vIer2YHZ2YCAzbSD2T0LrJO1OrMo3DGZH4H2lDoAq9317LykWxZ7OK1OVe2fQAx6Dv0ELZBt27BwmBoHdJ4V3zzG3SH3ycDaYBVKL2yYKbpIiE7JhlNWnL83ZDs3zgSaeGvfe6jjvyxJlyYkzUlQQZhXmUZp8OP9AIAK2qNV1QpuUPB03WZv94KYJc9M17z4WcfvJE0YOp3aejMXix6awWAdpvPC5E4A4Z6SmHYW8IxZXm0CJVu7oRLE91QxENX2LvtIsTMNoMzLuZQndLH31XeX7BvvPBtI0QlRZ3kJwnuMO0BoILxaceGuNM32Q5JKkcgnz1Yq8pYvytpvaSD2CIacuNUxQG3g5JrsUOTAC34vogfJX6kFZQogIDSBXKEUfBye70dFXGgi8eDsLEzVdzEL3aFNQ5w0MtN1XWke5GT25poQC3laqSHOG8"

    }    
    response = client.post('/posts/', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})  
    
    assert response.status_code==HTTPStatus.UNPROCESSABLE_ENTITY        
    assert "ensure this value has at most 777 characters" in response.json()["detail"][0]["msg"]

def test_should_allow_post_five_post_on_day(users, main_user_token):
    payload = {
        "post_type": "original",
        "text": "My 5 post"

    }    
    response = client.post('/posts/', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})  
    assert response.status_code==HTTPStatus.CREATED        

    response = client.get(f'/posts/{users[0]["username"]}?page=1')   
    assert response.status_code==HTTPStatus.OK    

    json_response =response.json()
    assert json_response["total_posts"] == 5

def test_should_deny_post_more_than_five_post_on_day(users, main_user_token):
    payload = {
        "post_type": "original",
        "text": "My 6 post"

    }    
    response = client.post('/posts/', json=payload, headers={"Authorization": f"Bearer {main_user_token}"})  
    
    assert response.status_code==HTTPStatus.FORBIDDEN
    assert "Daily user quote of 5 post reached" in response.json()["detail"]


def test_should_see_only_ten_posts_when_load_feed(users, main_user_token):
    payload = {
        "post_type": "original",
        "text": "My test original post"
    }    

    # genrate 5 posts for user 1 and 5 posts for user 2
    for i in range(10):
        if i % 2 == 0:
            response = client.post('/posts/', json=payload, headers={"Authorization": f"Bearer {generate_jwt(users[1]['username'])}"})  
        else:
            response = client.post('/posts/', json=payload, headers={"Authorization": f"Bearer {generate_jwt(users[2]['username'])}"})  
        assert response.status_code==HTTPStatus.CREATED

    response = client.get(f'/feeds/?page=1', headers={"Authorization": f"Bearer {generate_jwt(users[0]['username'])}"})   
    assert response.status_code==HTTPStatus.OK

    json_response =response.json()
    assert json_response["page_number"] == 1
    assert json_response["total_pages"] == 2
    assert json_response["total_posts"] == 15
    assert len(json_response["posts"]) == 10

    response = client.get(f'/feeds/?page=2', headers={"Authorization": f"Bearer {generate_jwt(users[0]['username'])}"})   
    assert response.status_code==HTTPStatus.OK

    json_response =response.json()
    assert json_response["page_number"] == 2
    assert json_response["total_pages"] == 2
    assert json_response["total_posts"] == 15
    assert len(json_response["posts"]) == 5

def test_should_see_only_followee_posts_when_load_feed(users, main_user_token):
    response = client.get(f'/feeds/?page=1&only_following=true', headers={"Authorization": f"Bearer {main_user_token}"})   
    assert response.status_code==HTTPStatus.OK

    json_response =response.json()
    assert json_response["page_number"] == 1
    assert json_response["total_pages"] == 1
    assert json_response["total_posts"] == 5
    assert len(json_response["posts"]) == 5

    