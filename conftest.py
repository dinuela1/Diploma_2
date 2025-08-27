import pytest
from data_gen import *


@pytest.fixture
def new_user():
    email = random_email()
    response = create_user(email)
    assert response.status_code == 200
    return {
        "email": email,
        "password": "123456",
        "token": response.json()["accessToken"]
    }


@pytest.fixture
def user_token(new_user):
    return new_user["token"]


@pytest.fixture
def user_credentials(new_user):
    return new_user["email"], new_user["password"]
