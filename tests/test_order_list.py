import requests
import allure
import data
from urls import ORDERS_URL


@allure.feature("Заказы")
@allure.story("Список заказов")
class TestOrderList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        with allure.step("Запрос на получение списка заказов"):
            response = requests.get(ORDERS_URL)

        with allure.step("Проверка структуры ответа"):
            allure.attach(
                response.text[:500] + "...", # Обрезаем огромный ответ для аттача
                name="Начало ответа сервера",
                attachment_type=allure.attachment_type.TEXT
            )
            assert response.status_code == data.ORDERS_LIST_SUCCESS_STATUS
            body = response.json()
            assert set(body.keys()) >= data.ORDERS_LIST_FIELDS
            assert isinstance(body["orders"], list)