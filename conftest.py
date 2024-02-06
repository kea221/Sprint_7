import pytest
import requests
import random
import string

from constants import Constants, Endpoints


@pytest.fixture
def create_and_then_delete_courier():

    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {"login": login, "password": password, "firstName": first_name}

    response = requests.post(f"{Constants.URL}{Endpoints.CREATE_COURIER}", data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    yield login_pass

    payload_login = {"login": login_pass[0], "password": login_pass[1]}
    response_id = requests.post(f"{Constants.URL}{Endpoints.LOGIN_COURIER}", data=payload_login)
    id_courier = response_id.json()["id"]
    response_del = requests.delete(f"{Constants.URL}/api/v1/courier/:{id_courier}")


@pytest.fixture()
def create_payload_and_then_delete_courier():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {"login": login, "password": password, "firstName": first_name}
    yield payload
    payload_login = {"login": login, "password": password}
    response_id = requests.post(f"{Constants.URL}{Endpoints.LOGIN_COURIER}", data=payload_login)
    id_courier = response_id.json()["id"]
    response_del = requests.delete(f"{Constants.URL}/api/v1/courier/:{id_courier}")
