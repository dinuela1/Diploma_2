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


@allure.title("Логин пользователя с корректными данными")
def test_login_success(user_credentials):
    email, password = user_credentials
    response = login_user(email, password)
    assert response.status_code == 200
    assert response.json()["success"] is True


@allure.title("Логин с неверным паролем")
def test_login_wrong_password(new_user):
    response = login_user(new_user["email"], "wrong_pass")
    assert response.status_code == 401
    assert response.json()["message"] == msg_incorrect_login_info


@allure.title("Создание заказа с авторизацией и валидными ингредиентами")
def test_create_order_with_auth(user_token):
    ingredients = ["61c0c5a71d1f82001bdaaa6d"]
    response = create_order(user_token, ingredients)
    assert response.status_code == 200
    assert response.json()["success"] is True


@allure.title("Создание заказа без авторизации")
def test_create_order_without_auth():
    ingredients = ["61c0c5a71d1f82001bdaaa6d"]
    response = create_order(None, ingredients)
    assert response.status_code == 200
    assert response.json()["success"] is True


@allure.title("Создание заказа без ингредиентов")
def test_create_order_without_ingredients(user_token):
    response = create_order(user_token, [])
    assert response.status_code == 400
    assert response.json()["message"] == msg_id_needed


@allure.title("Создание заказа с некорректным id ингредиента")
def test_create_order_with_wrong_hash(user_token):
    response = create_order(user_token, ["invalid_id"])
    assert response.status_code in (400, 500)
    assert response.json()["success"] is False
