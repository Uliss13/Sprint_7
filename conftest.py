import pytest
import requests
import allure
from api_client import (
    create_courier,
    login_courier,
    delete_courier,
    cancel_order,
)
from helpers import generate_courier_payload


@pytest.fixture
def courier():
    """Создаёт курьера перед тестом и удаляет после."""
    with allure.step("Подготовка: создание курьера"):
        payload = generate_courier_payload()
        response = create_courier(payload)
        
        if response.status_code != 201:
            pytest.skip(f"Не удалось создать курьера. Статус: {response.status_code}")

    yield payload

    with allure.step("Очистка: удаление курьера"):
        try:
            login_resp = login_courier({
                "login": payload["login"],
                "password": payload["password"]
            })
            if login_resp.status_code == 200:
                courier_id = login_resp.json().get("id")
                if courier_id:
                    delete_courier(courier_id)
        except requests.exceptions.RequestException:
            pass


@pytest.fixture
def cleanup_courier():
    """Собирает логины/пароли созданных в тесте курьеров и удаляет их после."""
    created = []

    def _add(login, password):
        created.append((login, password))

    yield _add

    with allure.step("Очистка: удаление созданных курьеров"):
        for login, password in created:
            try:
                resp = login_courier({"login": login, "password": password})
                if resp.status_code == 200:
                    cid = resp.json().get("id")
                    if cid:
                        delete_courier(cid)
            except requests.exceptions.RequestException:
                pass


@pytest.fixture
def cleanup_order():
    """Собирает треки созданных в тесте заказов и отменяет их после."""
    tracks = []

    def _add(track):
        tracks.append(track)

    yield _add

    with allure.step("Очистка: отмена созданных заказов"):
        for track in tracks:
            try:
                cancel_order(track)
            except requests.exceptions.RequestException:
                pass