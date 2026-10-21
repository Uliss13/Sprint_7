import allure
import requests
from urls import (
    COURIER_URL,
    LOGIN_COURIER_URL,
    ORDERS_URL,
    ORDERS_CANCEL_URL,
)

@allure.step("Отправка запроса на создание курьера")
def create_courier(payload):
    return requests.post(COURIER_URL, json=payload)

@allure.step("Отправка запроса на логин курьера")
def login_courier(payload):
    return requests.post(LOGIN_COURIER_URL, json=payload)

@allure.step("Удаление курьера по ID")
def delete_courier(courier_id):
    return requests.delete(f"{COURIER_URL}/{courier_id}")

@allure.step("Отправка запроса на создание заказа")
def create_order(payload):
    return requests.post(ORDERS_URL, json=payload)

@allure.step("Получение списка заказов")
def get_orders():
    return requests.get(ORDERS_URL)

@allure.step("Отмена заказа по треку")
def cancel_order(track):
    return requests.put(f"{ORDERS_CANCEL_URL}?track={track}")