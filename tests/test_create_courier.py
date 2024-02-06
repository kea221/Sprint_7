import requests
from faker import Faker
import allure

from constants import Constants, Endpoints

faker = Faker()


class TestCreateCourier:
    @allure.title("Курьера можно создать")
    def test_new_courier_created(self, create_payload_and_then_delete_courier):
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_COURIER}",
                                 data=create_payload_and_then_delete_courier)
        print(create_payload_and_then_delete_courier)
        assert response.status_code == 201
        assert response.text == '{"ok":true}'

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_the_same_courier_not_created(self, create_payload_and_then_delete_courier):
        response_first = requests.post(f"{Constants.URL}{Endpoints.CREATE_COURIER}",
                                       data=create_payload_and_then_delete_courier)
        response_second = requests.post(f"{Constants.URL}{Endpoints.CREATE_COURIER}",
                                        data=create_payload_and_then_delete_courier)
        assert response_second.status_code == 409
        assert response_second.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Нельзя создать курьера без логина")
    def test_courier_without_login_not_created(self):
        payload = {"login": "",
                   "password": faker.password,
                   "firstName": faker.first_name}
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_COURIER}", data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Нельзя создать курьера без пароля")
    def test_courier_without_password_not_created(self):
        payload = {"login": faker.user_name,
                   "password": "",
                   "firstName": faker.first_name}
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_COURIER}", data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
