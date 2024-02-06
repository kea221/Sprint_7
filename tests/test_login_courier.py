import requests
import allure

from constants import Constants, Endpoints


class TestLoginCourier:
    @allure.title("Курьер может авторизоваться")
    def test_courier_logn_successful(self, create_and_then_delete_courier):
        payload = {"login": create_and_then_delete_courier[0],
                   "password": create_and_then_delete_courier[1],
                   "firstName": create_and_then_delete_courier[2]}
        response = requests.post(f"{Constants.URL}{Endpoints.LOGIN_COURIER}", data=payload)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Не происходит авторизация курьером, если не передан пароль")
    def test_courier_dont_login_without_password(self, create_and_then_delete_courier):
        payload = {"login": create_and_then_delete_courier[0],
                   "password": "",
                   "firstName": create_and_then_delete_courier[2]}
        response = requests.post(f"{Constants.URL}{Endpoints.LOGIN_COURIER}", data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Не происходит авторизация курьером, если не передан логин")
    def test_courier_dont_login_without_login(self, create_and_then_delete_courier):
        payload = {"login": "",
                   "password": create_and_then_delete_courier[1],
                   "firstName": create_and_then_delete_courier[2]}
        response = requests.post(f"{Constants.URL}{Endpoints.LOGIN_COURIER}", data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Не происходит авторизация курьером, если передан неверный логин")
    def test_courier_dont_login_with_invalid_login(self, create_and_then_delete_courier):
        payload = {"login": "vasya123",
                   "password": create_and_then_delete_courier[1],
                   "firstName": create_and_then_delete_courier[2]}
        response = requests.post(f"{Constants.URL}{Endpoints.LOGIN_COURIER}", data=payload)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Не происходит авторизация курьером, если передан неверный пароль")
    def test_courier_dont_login_with_invalid_password(self, create_and_then_delete_courier):
        payload = {"login": create_and_then_delete_courier[0],
                   "password": "5555v",
                   "firstName": create_and_then_delete_courier[2]}
        response = requests.post(f"{Constants.URL}{Endpoints.LOGIN_COURIER}", data=payload)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Не происходит авторизация несуществующим курьером")
    def test_unregistered_courier_dont_login(self):
        payload = {"login": "on_zhe_zhora",
                   "password": "8989",
                   "firstName": "goga"}
        response = requests.post(f"{Constants.URL}{Endpoints.LOGIN_COURIER}", data=payload)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
