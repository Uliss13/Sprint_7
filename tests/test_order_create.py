import pytest
import allure
import data
from api_client import create_order


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
    def test_create_order(self, cleanup_order, color):
        with allure.step(f"Создание заказа с параметрами цвета: {color}"):
            payload = data.ORDER_PAYLOAD.copy()
            payload["color"] = color
            response = create_order(payload)
            body = response.json()

            cleanup_order(body.get("track"))

        with allure.step("Проверка успешного создания и наличия track"):
            assert response.status_code == data.ORDER_CREATE_SUCCESS_STATUS
            assert "track" in body