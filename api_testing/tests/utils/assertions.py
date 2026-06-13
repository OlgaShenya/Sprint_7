import allure


@allure.step("Проверить статус-код ответа: {expected_code}")
def assert_status_code(response, expected_code):
    assert response.status_code == expected_code


@allure.step("Проверить ошибку: код {expected_code}, сообщение «{expected_message}»")
def assert_error_response(response, expected_code, expected_message):
    assert_status_code(response, expected_code)
    assert response.json()["message"] == expected_message


@allure.step("Проверить успешное создание курьера")
def assert_courier_create_success(response):
    assert_status_code(response, 201)
    assert response.json() == {"ok": True}


@allure.step("Проверить ошибку: недостаточно данных для создания курьера")
def assert_courier_create_missing_fields(response):
    assert_error_response(
        response,
        400,
        "Недостаточно данных для создания учетной записи",
    )


@allure.step("Проверить ошибку: логин уже используется")
def assert_courier_create_duplicate_login(response):
    assert_status_code(response, 409)
    assert "Этот логин уже используется" in response.json()["message"]


@allure.step("Проверить успешную авторизацию курьера")
def assert_courier_login_success(response):
    assert_status_code(response, 200)
    response_json = response.json()
    assert "id" in response_json
    assert isinstance(response_json["id"], int)


@allure.step("Проверить ошибку: недостаточно данных для входа")
def assert_courier_login_missing_fields(response):
    assert_error_response(response, 400, "Недостаточно данных для входа")


@allure.step("Проверить ошибку: учётная запись не найдена")
def assert_courier_login_not_found(response):
    assert_error_response(response, 404, "Учетная запись не найдена")


@allure.step("Проверить успешное создание заказа")
def assert_order_create_success(response, test_name=None):
    prefix = f"Test '{test_name}': " if test_name else ""
    response_json = response.json()
    assert_status_code(response, 201)
    
    assert "track" in response_json, f"{prefix}track not found in response"
    assert isinstance(response_json["track"], int), f"{prefix}track is not an integer"


@allure.step("Проверить структуру успешного ответа списка заказов")
def assert_orders_response_success(response):
    assert_status_code(response, 200)
    response_json = response.json()
    assert "orders" in response_json
    assert isinstance(response_json["orders"], list)
    assert "pageInfo" in response_json
    assert isinstance(response_json["pageInfo"], dict)
    assert "availableStations" in response_json
    assert isinstance(response_json["availableStations"], list)
    return response_json


@allure.step("Проверить структуру pageInfo")
def assert_page_info_structure(page_info):
    assert "page" in page_info
    assert "total" in page_info
    assert "limit" in page_info
    assert isinstance(page_info["page"], int)
    assert isinstance(page_info["total"], int)
    assert isinstance(page_info["limit"], int)


ORDER_FIELDS = (
    "id",
    "track",
    "firstName",
    "lastName",
    "address",
    "metroStation",
    "phone",
    "rentTime",
    "deliveryDate",
    "color",
)


@allure.step("Проверить структуру заказа в списке")
def assert_order_in_list_structure(order):
    for field in ORDER_FIELDS:
        assert field in order


@allure.step("Проверить структуру станции в availableStations")
def assert_available_station_structure(station):
    assert "name" in station
    assert "number" in station
    assert "color" in station
