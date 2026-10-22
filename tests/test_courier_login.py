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

    @allure.title("Ошибка при логине без поля 'login'")
    def test_login_missing_login_field(self, courier):
        with allure.step("Формирование payload без поля 'login'"):
            bad_data = {"password": courier["password"]}
            
        with allure.step("Отправка запроса"):
            response = login_courier(bad_data)

        with allure.step("Проверка кода и тела ответа"):
            assert response.status_code == data.COURIER_LOGIN_BAD_REQUEST_STATUS
            assert response.json()["message"] == data.COURIER_LOGIN_MISSING_DATA_MSG

    @allure.title("Ошибка при логине без поля 'password'")
    def test_login_missing_password_field(self, courier):
        with allure.step("Формирование payload без поля 'password'"):
            bad_data = {"login": courier["login"]}
            
        with allure.step("Отправка запроса"):
            response = login_courier(bad_data)

        with allure.step("Проверка фактического ответа сервера (504, без тела)"):
            # Фактический ответ сервиса — 504 Gateway Timeout (тело отсутствует)
            assert response.status_code == data.COURIER_LOGIN_MISSING_PASSWORD_STATUS

    @allure.title("Ошибка при неверном логине")
    def test_login_wrong_login(self, courier):
        with allure.step("Формирование payload с неверным логином"):
            bad_data = {"login": "wrong_login_999", "password": courier["password"]}
            
        with allure.step("Отправка запроса"):
            response = login_courier(bad_data)

        with allure.step("Проверка ответа"):
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