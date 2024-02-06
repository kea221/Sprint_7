import pytest
import requests
import allure
import random

from constants import Constants, Endpoints
from faker import Faker

faker = Faker("ru_Ru")


class TestOrder:
    @allure.title("Можно создать заказ с разными вариантами цвета самоката")
    @pytest.mark.parametrize("color", Constants.COLOR_LIST)
    def test_create_order_successful(self, color):
        payload = {"firstName": faker.first_name,
                   "lastName": faker.last_name,
                   "address": faker.street_address,
                   "metroStation": random.randint(1, 224),
                   "phone": faker.phone_number,
                   "rentTime": random.randint(1, 7),
                   "deliveryDate": faker.date_time_between(start_date="now", end_date="+10d"),
                   "comment": faker.sentence,
                   "color": color}
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_ORDER}", data=payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("В теле ответа возвращается список заказов")
    def test_get_order_list(self):
        payload = {"firstName": faker.first_name,
                   "lastName": faker.last_name,
                   "address": faker.street_address,
                   "metroStation": random.randint(1, 224),
                   "phone": faker.phone_number,
                   "rentTime": random.randint(1, 7),
                   "deliveryDate": faker.date_time_between(start_date="now", end_date="+10d"),
                   "comment": faker.sentence,
                   "color": random.choice(Constants.COLOR_LIST)}
        response_first = requests.post(f"{Constants.URL}{Endpoints.CREATE_ORDER}", data=payload)
        response_second = requests.post(f"{Constants.URL}{Endpoints.CREATE_ORDER}", data=payload)
        response_third = requests.post(f"{Constants.URL}{Endpoints.CREATE_ORDER}", data=payload)

        response_get = requests.get(f"{Constants.URL}{Endpoints.GET_ORDER_LIST}")
        assert response_get.status_code == 200
        assert "orders" in response_get.json()
