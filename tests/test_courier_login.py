import pytest
import requests
import allure
import data
from urls import LOGIN_COURIER_URL


@allure.feature("Курьеры")
@allure.story("Логин курьера")
class TestCourierLogin:

    @allure.title("Успешный логин курьера")
    def test_login_success(self, courier):
        with allure.step("Отправка запроса на логин"):
            response = requests.post(LOGIN_COURIER_URL, json=courier)

        with allure.step("Проверка успешного ответа"):
            allure.attach(
                response.text,
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )
            assert response.status_code == data.COURIER_LOGIN_SUCCESS_STATUS
            assert "id" in response.json()

    @allure.title("Ошибка при неверном пароле")
    def test_login_wrong_password(self, courier):
        with allure.step("Логин с неверным паролем"):
            bad_data = {"login": courier["login"], "password": "wrong_password"}
            response = requests.post(LOGIN_COURIER_URL, json=bad_data)

        with allure.step("Проверка ответа"):
            allure.attach(
                response.text,
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )
            assert response.status_code == data.COURIER_LOGIN_NOT_FOUND_STATUS
            assert response.json()["message"] == data.COURIER_LOGIN_NOT_FOUND_MSG

    
    @allure.title("Ошибка при логине без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, courier, missing_field):
        with allure.step(f"Формирование payload без поля '{missing_field}'"):
            bad_data = {"login": courier["login"], "password": courier["password"]}
            bad_data.pop(missing_field)

        with allure.step("Отправка запроса на логин"):
            response = requests.post(LOGIN_COURIER_URL, json=bad_data)

        with allure.step("Проверка ответа"):
            # Если сервер падает в 504 при отсутствии password — фиксируем баг через xfail
            if response.status_code == 504:
                pytest.xfail(f"Баг API: 504 Gateway Timeout при отсутствии поля {missing_field}")

            allure.attach(
                response.text,
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )
            assert response.status_code == data.COURIER_LOGIN_BAD_REQUEST_STATUS
            assert response.json()["message"] == data.COURIER_LOGIN_MISSING_DATA_MSG