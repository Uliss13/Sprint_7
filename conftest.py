import pytest
import requests
import allure
import json
from urls import COURIER_URL, LOGIN_COURIER_URL
from helpers import register_new_courier_and_return_login_password


@pytest.fixture
def courier():
    with allure.step("Подготовка: создание курьера"):
        courier_data = register_new_courier_and_return_login_password()

        if not courier_data:
            pytest.skip("Не удалось создать курьера для теста")

        login, password = courier_data[0], courier_data[1]
        allure.attach(
            json.dumps({"login": login, "password": password}, indent=2),
            name="Данные созданного курьера",
            attachment_type=allure.attachment_type.JSON
        )

    yield {"login": login, "password": password}

    with allure.step("Очистка: удаление курьера"):
        try:
            login_resp = requests.post(LOGIN_COURIER_URL, json={"login": login, "password": password}, timeout=5)
            if login_resp.status_code == 200:
                courier_id = login_resp.json().get("id")
                if courier_id:
                    delete_resp = requests.delete(f"{COURIER_URL}/{courier_id}", timeout=5)
                    allure.attach(
                                f"Удалён курьер ID={courier_id}, статус={delete_resp.status_code}",
                                name="Результат удаления",
                                attachment_type=allure.attachment_type.TEXT
                    )
        except requests.exceptions.RequestException as e:
            # Если сервер упал во время очистки — логируем это в отчёт, не роняя тест
            allure.attach(str(e), name="Ошибка при очистке", attachment_type=allure.attachment_type.TEXT)
                