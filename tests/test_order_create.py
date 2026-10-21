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
            # Копируем базовый payload и добавляем цвет, чтобы не менять оригинал в data.py
            payload = data.ORDER_PAYLOAD.copy()
            payload["color"] = color
            
            response = create_order(payload)

        with allure.step("Проверка успешного создания и наличия track"):
            assert response.status_code == data.ORDER_CREATE_SUCCESS_STATUS
            body = response.json()
            assert "track" in body
            
            # Регистрируем трек для отмены (очистка)
            cleanup_order(body["track"])