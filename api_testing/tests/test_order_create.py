import allure
import pytest

from api_testing.tests.utils.assertions import assert_order_create_success


@allure.title("Создание заказа: {test_name}")
@allure.description("Проверка кода 201 и наличия track в ответе")
@pytest.mark.parametrize(
    "test_name,color",
    [
        ("BLACK only", ["BLACK"]),
        ("GREY only", ["GREY"]),
        ("Both colors", ["BLACK", "GREY"]),
        ("No color", None),
    ],
)
class TestOrderCreate:
    def test_create_order_with_color_returns_201(self, order_api_client, valid_order_payload, test_name, color):
        payload = valid_order_payload.copy()
        if color is not None:
            payload["color"] = color
        response = order_api_client.create(payload)
        assert_order_create_success(response, test_name=test_name)
