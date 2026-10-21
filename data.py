
# Курьер: создание
COURIER_CREATE_SUCCESS_STATUS = 201
COURIER_CREATE_DUPLICATE_STATUS = 409
COURIER_CREATE_DUPLICATE_MSG = "Этот логин уже используется. Попробуйте другой."
COURIER_CREATE_BAD_REQUEST_STATUS = 400
COURIER_CREATE_MISSING_DATA_MSG = "Недостаточно данных для создания учетной записи"

# Курьер: логин
COURIER_LOGIN_SUCCESS_STATUS = 200
COURIER_LOGIN_BAD_REQUEST_STATUS = 400
COURIER_LOGIN_MISSING_DATA_MSG = "Недостаточно данных для входа"
COURIER_LOGIN_NOT_FOUND_STATUS = 404
COURIER_LOGIN_NOT_FOUND_MSG = "Учетная запись не найдена"
# Курьер: логин (дополнения)
COURIER_LOGIN_MISSING_PASSWORD_STATUS = 504  # Фактический ответ сервиса (известная недоработка)


# Данные несуществующего курьера для теста логина
NONEXISTENT_COURIER = {
    "login": "nonexistent_user_123",
    "password": "some_password"
}

# Заказы: цвета
COLOR_BLACK = "BLACK"
COLOR_GREY = "GREY"

# Заказы: создание
ORDER_CREATE_SUCCESS_STATUS = 201

# Заказы: список
ORDERS_LIST_SUCCESS_STATUS = 200
ORDERS_LIST_FIELDS = {"orders", "pageInfo"}

# Данные для создания заказа
ORDER_PAYLOAD = {
    "firstName": "Test",
    "lastName": "Test",
    "address": "Moscow, ul. Pushkina, 1",
    "metroStation": 4,
    "phone": "+79990000000",
    "rentTime": 5,
    "deliveryDate": "2026-10-20",
    "comment": "Test comment",
}
