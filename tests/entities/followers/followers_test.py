import pytest
from twijournal.entities.followers.schema import FollowerSchema
from datetime import datetime
from pydantic import ValidationError

def test_should_insert_follower_successfully_when_all_data_is_correct():
    follower = FollowerSchema(
        followee_id=1,
        follower_id=2,
        created_at=datetime.now()
    )
    assert follower.followee_id == 1
    assert follower.follower_id == 2

def test_should_fail_when_user_and_followers_are_the_same_person():
    with pytest.raises(ValidationError) as execinfo:
        follower = FollowerSchema(
            followee_id=1,
            follower_id=1,
            created_at=datetime.now()
        )
    assert "user can't follow himself" in str(execinfo.value)


