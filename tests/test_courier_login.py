import pytest
import allure
import data
from api_client import login_courier


@allure.feature("Курьеры")
@allure.story("Логин курьера")
class TestCourierLogin:

    @allure.title("Успешный логин курьера")
    def test_login_success(self, courier):
        with allure.step("Отправка запроса на логин"):
            response = login_courier(courier)

        with allure.step("Проверка ответа"):
            assert response.status_code == data.COURIER_LOGIN_SUCCESS_STATUS
            assert "id" in response.json()

    @allure.title("Ошибка при логине без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field, expected_status", [
        ("login", data.COURIER_LOGIN_BAD_REQUEST_STATUS),
        ("password", data.COURIER_LOGIN_MISSING_PASSWORD_STATUS),
    ], ids=["login_empty", "password_empty"])
    def test_login_missing_field(self, courier, missing_field, expected_status):
        with allure.step(f"Формирование payload без поля '{missing_field}'"):
            bad_data = {"login": courier["login"], "password": courier["password"]}
            bad_data.pop(missing_field)

        with allure.step("Отправка запроса"):
            response = login_courier(bad_data)

        with allure.step("Проверка фактического ответа сервера"):
            assert response.status_code == expected_status

    @allure.title("Ошибка при неверном логине")
    def test_login_wrong_login(self, courier):
        bad_data = {"login": "wrong_login_999", "password": courier["password"]}
        response = login_courier(bad_data)
        assert response.status_code == data.COURIER_LOGIN_NOT_FOUND_STATUS
        assert response.json()["message"] == data.COURIER_LOGIN_NOT_FOUND_MSG

    @allure.title("Ошибка при неверном пароле")
    def test_login_wrong_password(self, courier):
        with allure.step("Логин с неверным паролем"):
            bad_data = {"login": courier["login"], "password": "wrong_password"}
            response = login_courier(bad_data)

        with allure.step("Проверка ответа"):
            assert response.status_code == data.COURIER_LOGIN_NOT_FOUND_STATUS
            assert response.json()["message"] == data.COURIER_LOGIN_NOT_FOUND_MSG

    @allure.title("Ошибка при несуществующем логине")
    def test_login_nonexistent_user(self):
        with allure.step("Логин под несуществующим пользователем"):
            response = login_courier(data.NONEXISTENT_COURIER)

        with allure.step("Проверка ответа"):
            assert response.status_code == data.COURIER_LOGIN_NOT_FOUND_STATUS
            assert response.json()["message"] == data.COURIER_LOGIN_NOT_FOUND_MSG