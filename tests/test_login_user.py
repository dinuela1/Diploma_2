import allure
from data_gen import *
from data_check import *


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


@allure.title("Логин с неверным логином")
def test_login_wrong_email(new_user):
    response = login_user("no_email_at_all@mail.ru", new_user["password"])
    assert response.status_code == 401
    assert response.json()["message"] == msg_incorrect_login_info
