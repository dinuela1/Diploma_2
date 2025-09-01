import allure
from data_gen import *
from data_check import *


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