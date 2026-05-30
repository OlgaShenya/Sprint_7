import allure
import pytest

from api_testing.tests.utils.assertions import (
    assert_courier_create_duplicate_login,
    assert_courier_create_missing_fields,
    assert_courier_create_success,
)


@allure.title("Успешное создание курьера")
@allure.description("Проверка кода 201 и тела ответа")
class TestCourierCreate:
    def test_create_courier_valid_data_returns_201(self, api_client, valid_payload):
        response = api_client.create(valid_payload)
        assert_courier_create_success(response)


    @allure.title("Создание курьера без обязательного поля: {missing_field}")
    @allure.description("Проверка кода 400 и сообщения об ошибке")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field_returns_400(self, api_client, valid_payload, missing_field):
        payload = valid_payload.copy()
        del payload[missing_field]
        response = api_client.create(payload)
        assert_courier_create_missing_fields(response)


    @allure.title("Создание курьера без поля firstName")
    @allure.description(
        "По документации ожидается 400, по факту API принимает запрос и возвращает 201. "
        "Тест проверяет реальное поведение."
    )
    def test_create_courier_without_first_name_returns_201(self, api_client, valid_payload):
        payload = valid_payload.copy()
        del payload["firstName"]
        response = api_client.create(payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}


    @allure.title("Повторное создание курьера с тем же логином")
    @allure.description("Проверка кода 409 Conflict")
    def test_create_courier_duplicate_login_returns_409(self, api_client, valid_payload):
        api_client.create(valid_payload)
        response = api_client.create(valid_payload)
        assert_courier_create_duplicate_login(response)
