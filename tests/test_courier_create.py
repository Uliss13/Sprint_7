import pytest
import requests
import allure
import json
import data
from urls import COURIER_URL
from helpers import register_new_courier_and_return_login_password


@allure.feature("Курьеры")
@allure.story("Создание курьера")
class TestCourierCreate:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        with allure.step("Создание нового курьера через хелпер"):
            courier_data = register_new_courier_and_return_login_password()
            allure.attach(
                json.dumps(courier_data, indent=2),
                name="Данные созданного курьера",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что курьер создан"):
            assert len(courier_data) == 3, "Курьер не создан (вернулся пустой список)"

    @allure.title("Ошибка при создании дубликата курьера")
    def test_create_courier_duplicate(self):
        with allure.step("Создание первого курьера"):
            courier_data = register_new_courier_and_return_login_password()
            login, password = courier_data[0], courier_data[1]

        with allure.step("Попытка создать курьера с тем же логином"):
            payload = {"login": login, "password": password}
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверка кода и сообщения об ошибке"):
            allure.attach(
                response.text,
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )
            assert response.status_code == data.COURIER_CREATE_DUPLICATE_STATUS
            assert response.json()["message"] == data.COURIER_CREATE_DUPLICATE_MSG

    @allure.title("Ошибка при создании курьера без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        with allure.step(f"Формирование payload без поля '{missing_field}'"):
            payload = {
                "login": "test_login_123",
                "password": "test_password_123",
                "firstName": "Test"
            }
            payload.pop(missing_field)
            allure.attach(
                json.dumps(payload, indent=2),
                name="Отправленный payload",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Отправка запроса на создание курьера"):
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверка кода и сообщения об ошибке"):
            allure.attach(
                response.text,
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )
            assert response.status_code == data.COURIER_CREATE_BAD_REQUEST_STATUS
            assert response.json()["message"] == data.COURIER_CREATE_MISSING_DATA_MSG