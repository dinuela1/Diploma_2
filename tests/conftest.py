import pytest
from data_gen import *


@pytest.fixture
def new_user():
    email = random_email()
    response = create_user(email)
    token = response.json()["accessToken"]
    user = {
        "email": email,
        "password": "123456",
        "token": token
    }
    yield user
    requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": token})


@pytest.fixture
def user_token(new_user):
    return new_user["token"]


@pytest.fixture
def user_credentials(new_user):
    return new_user["email"], new_user["password"]
