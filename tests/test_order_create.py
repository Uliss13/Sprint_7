import pytest
import requests
import allure
import data
from urls import ORDERS_URL


@allure.feature("Заказы")
@allure.story("Создание заказа")
class TestOrderCreate:

    @allure.title("Создание заказа с цветом: {color}")
    @pytest.mark.parametrize("color", [
        [data.COLOR_BLACK],
        [data.COLOR_GREY],
        [data.COLOR_BLACK, data.COLOR_GREY],
        []
    ])
    def test_create_order(self, color):
        with allure.step(f"Создание заказа с параметрами цвета: {color}"):
            payload = {
                "firstName": "Test",
                "lastName": "Test",
                "address": "Moscow",
                "metroStation": 4,
                "phone": "+79990000000",
                "rentTime": 5,
                "deliveryDate": "2026-10-20",
                "comment": "Test comment",
                "color": color
            }
            response = requests.post(ORDERS_URL, json=payload)

        with allure.step("Проверка успешного создания и наличия track"):
            allure.attach(
                response.text,
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )
            assert response.status_code == data.ORDER_CREATE_SUCCESS_STATUS
            assert "track" in response.json()