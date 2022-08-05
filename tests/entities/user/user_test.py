import pytest
from twijournal.entities.user.schema import UserSchema
from datetime import datetime
from pydantic import ValidationError

def test_should_insert_user_successfully_when_all_data_is_correct():
    user = UserSchema(
        id=1,
        username="username",
        email="user@email.com",
        created_at=datetime.now()
    )
    assert user.id == 1
    assert user.username == "username"
    assert user.email == "user@email.com"

def test_should_fail_when_username_greater_than_permitted():
    with pytest.raises(ValidationError) as execinfo:
        user = UserSchema(
            id=1,
            username="userUsernameIsGreaterThanPermitted",
            email="user@email.com",
            created_at=datetime.now()
        )
    
    assert "ensure this value has at most 14 characters" in str(execinfo.value)

def test_should_fail_when_username_is_not_alphanumeric():
    with pytest.raises(ValidationError) as execinfo:
        user = UserSchema(
            id=1,
            username="!3!.user",
            email="user@email.com",
            created_at=datetime.now()
        )
    
    assert 'string does not match regex "^[a-zA-Z0-9]+$"' in str(execinfo.value)    

def test_should_fail_when_created_at_is_empty():
    with pytest.raises(ValidationError) as execinfo:
        user = UserSchema(
            id=1,
            username="user",
            email="user@email.com"
        )
    
    assert 'field required' in str(execinfo.value)        