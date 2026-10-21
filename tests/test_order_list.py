import allure
import data
from api_client import get_orders


@allure.feature("Заказы")
@allure.story("Список заказов")
class TestOrderList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        with allure.step("Запрос на получение списка заказов"):
            response = get_orders()

        with allure.step("Проверка структуры ответа"):
            assert response.status_code == data.ORDERS_LIST_SUCCESS_STATUS
            body = response.json()
            assert set(body.keys()) >= data.ORDERS_LIST_FIELDS
            assert isinstance(body["orders"], list)