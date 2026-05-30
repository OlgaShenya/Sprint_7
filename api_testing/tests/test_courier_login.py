import allure
import pytest
import requests

from api_testing.tests.utils.assertions import (
    assert_courier_login_missing_fields,
    assert_courier_login_not_found,
    assert_courier_login_success,
)


@allure.title("Успешная авторизация курьера")
@allure.description("Проверка кода 200 и наличия id в ответе")
class TestCourierLogin:
    def test_login_valid_credentials_returns_200(self, api_client, created_courier_payload):
        response = api_client.login(created_courier_payload)
        assert_courier_login_success(response)


    @allure.title("Авторизация без обязательного поля: {missing_field}")
    @allure.description("Проверка кода 400 и сообщения об ошибке")
    @pytest.mark.parametrize("missing_field", ["login"])
    def test_login_without_required_field_returns_400(self, api_client, created_courier_payload, missing_field):
        payload = created_courier_payload.copy()
        del payload[missing_field]
        response = api_client.login(payload)
        assert_courier_login_missing_fields(response)


    @allure.title("Авторизация без поля password")
    @allure.description(
        "По документации ожидается 400, по факту сервер зависает и не отвечает — "
        "клиент получает ReadTimeout."
    )
    def test_login_without_password_server_hangs(self, api_client, created_courier_payload):
        payload = created_courier_payload.copy()
        del payload["password"]
        with pytest.raises(requests.exceptions.ReadTimeout):
            api_client.login(payload, timeout=60)


    @allure.title("Авторизация с неверным паролем")
    @allure.description("Проверка кода 404 и сообщения «Учетная запись не найдена»")
    def test_login_wrong_password_returns_404(self, api_client, created_courier_payload):
        wrong_payload = created_courier_payload.copy()
        wrong_payload["password"] = "WrongPassword123"
        response = api_client.login(wrong_payload)
        assert_courier_login_not_found(response)


    @allure.title("Авторизация с неверным логином")
    @allure.description("Проверка кода 404 и сообщения «Учетная запись не найдена»")
    def test_login_wrong_login_returns_404(self, api_client, created_courier_payload):
        wrong_payload = created_courier_payload.copy()
        wrong_payload["login"] = "completely_wrong_login_xyz"
        response = api_client.login(wrong_payload)
        assert_courier_login_not_found(response)


    @allure.title("Авторизация несуществующего пользователя")
    @allure.description("Проверка кода 404 и сообщения «Учетная запись не найдена»")
    def test_login_nonexistent_user_returns_404(self, api_client, valid_payload):
        wrong_payload = valid_payload.copy()
        wrong_payload["login"] = "nonexistent_user_12345"
        response = api_client.login(wrong_payload)
        assert_courier_login_not_found(response)
