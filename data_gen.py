import requests
import random
import string
from url import *


def random_email():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(8)) + "@test.ru"


def create_user(email, password="123456", name="TestUser"):
    return requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": password,
        "name": name
    })


def login_user(email, password):
    return requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })


def create_order(token=None, ingredients=None):
    headers = {"Authorization": token} if token else {}
    body = {"ingredients": ingredients} if ingredients else {}
    return requests.post(f"{BASE_URL}/orders", headers=headers, json=body)
