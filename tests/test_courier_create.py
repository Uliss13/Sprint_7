import pytest
import allure
import requests
import data
from urls import COURIER_URL
from helpers import generate_courier_payload
from api_client import create_courier


@allure.feature("Курьеры")
@allure.story("Создание курьера")
class TestCourierCreate:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, cleanup_courier):
        with allure.step("Формирование данных и запрос на создание"):
            payload = generate_courier_payload()
            response = create_courier(payload)
            
            # Регистрируем для очистки, если создался
            if response.status_code == 201:
                cleanup_courier(payload["login"], payload["password"])

        with allure.step("Проверка кода и тела ответа"):
            assert response.status_code == data.COURIER_CREATE_SUCCESS_STATUS
            assert response.json() == {"ok": True}

    @allure.title("Ошибка при создании дубликата курьера (полное совпадение)")
    def test_create_courier_duplicate(self, cleanup_courier):
        with allure.step("Создание первого курьера"):
            payload = generate_courier_payload()
            response_1 = create_courier(payload)
            assert response_1.status_code == 201
            cleanup_courier(payload["login"], payload["password"])

        with allure.step("Попытка создать точно такого же курьера"):
            response_2 = create_courier(payload)

        with allure.step("Проверка кода и текста ошибки"):
            assert response_2.status_code == data.COURIER_CREATE_DUPLICATE_STATUS
            assert response_2.json()["message"] == data.COURIER_CREATE_DUPLICATE_MSG

    @allure.title("Ошибка при создании курьера без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        with allure.step(f"Формирование payload без поля '{missing_field}'"):
            payload = generate_courier_payload()
            payload.pop(missing_field)

        with allure.step("Отправка запроса"):
            response = create_courier(payload)

        with allure.step("Проверка кода и сообщения"):
            assert response.status_code == data.COURIER_CREATE_BAD_REQUEST_STATUS
            assert response.json()["message"] == data.COURIER_CREATE_MISSING_DATA_MSG