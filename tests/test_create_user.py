import pytest
import allure
from data_gen import *
from data_check import *


@allure.title("Создание уникального пользователя")
def test_create_new_user():
    email = random_email()
    response = create_user(email)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert asses_token in response.json()


@allure.title("Создание пользователя с уже существующим email")
def test_create_existing_user(new_user):
    response = create_user(new_user["email"])
    assert response.status_code == 403
    assert response.json()["message"] == msg_user_exists


@pytest.mark.parametrize("missing_field", ["email", "password", "name"])
@allure.title("Создание пользователя без обязательного поля {missing_field}")
def test_create_user_without_required_field(missing_field):
    data = {"email": random_email(), "password": "123456", "name": "User"}
    data.pop(missing_field)
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    assert response.status_code == 403
    assert response.json()["message"] == msg_missing_field

