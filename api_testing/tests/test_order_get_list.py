import allure
import pytest

from api_testing.tests.utils.assertions import (
    assert_available_station_structure,
    assert_error_response,
    assert_order_in_list_structure,
    assert_orders_response_success,
    assert_page_info_structure,
)


@allure.title("Получение списка заказов без параметров")
@allure.description("Проверка кода 200 и структуры ответа")
class TestOrderGetList:
    def test_get_orders_without_params_returns_200(self, order_api_client):
        response = order_api_client.get_orders()
        assert_orders_response_success(response)


    @allure.title("Проверка структуры pageInfo")
    @allure.description("Проверка полей page, total, limit")
    def test_get_orders_page_info_has_required_fields(self, order_api_client):
        response = order_api_client.get_orders()
        response_json = assert_orders_response_success(response)
        assert_page_info_structure(response_json["pageInfo"])


    @allure.title("Проверка структуры заказа в списке")
    @allure.description("Создание заказа и проверка полей в списке orders")
    def test_get_orders_order_has_required_fields(self, order_api_client):
        order_payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test Address",
            "metroStation": 1,
            "phone": "+7 999 999 99 99",
            "rentTime": 1,
            "deliveryDate": "2025-01-01",
            "comment": "Test order",
            "color": ["BLACK"],
        }
        order_api_client.create(order_payload)

        response = order_api_client.get_orders()
        response_json = assert_orders_response_success(response)
        assert_order_in_list_structure(response_json["orders"][0])


    @allure.title("Фильтрация по валидному courierId")
    @allure.description("Проверка кода 200 и структуры ответа")
    def test_get_orders_by_valid_courier_id_returns_200(self, order_api_client, valid_courier_id):
        response = order_api_client.get_orders(courier_id=valid_courier_id)
        assert_orders_response_success(response)


    @allure.title("Фильтрация по несуществующему courierId")
    @allure.description("Проверка кода 404 и сообщения об ошибке")
    def test_get_orders_nonexistent_courier_returns_404(self, order_api_client):
        response = order_api_client.get_orders(courier_id=999999)
        assert_error_response(
            response,
            404,
            "Курьер с идентификатором 999999 не найден",
        )


    @allure.title("Фильтрация по станциям метро: {stations}")
    @allure.description("Проверка кода 200 и структуры ответа")
    @pytest.mark.parametrize("stations", ['["1"]', '["2"]', '["1", "2"]'])
    def test_get_orders_by_nearest_station_returns_200(self, order_api_client, valid_courier_id, stations):
        response = order_api_client.get_orders(
            courier_id=valid_courier_id,
            nearest_station=stations,
        )
        assert_orders_response_success(response)


    @allure.title("Пагинация: limit={limit_value}")
    @allure.description("Проверка количества заказов и значения limit в pageInfo")
    @pytest.mark.parametrize("limit_value", [1, 5, 10, 20, 30])
    def test_get_orders_with_limit_returns_correct_count(self, order_api_client, limit_value):
        response = order_api_client.get_orders(limit=limit_value, page=0)
        response_json = assert_orders_response_success(response)

        assert len(response_json["orders"]) <= limit_value
        assert response_json["pageInfo"]["limit"] == limit_value


    @allure.title("Пагинация: page={page_value}")
    @allure.description("Проверка номера страницы в pageInfo")
    @pytest.mark.parametrize("page_value", [0, 1, 2])
    def test_get_orders_with_page_returns_correct_page(self, order_api_client, page_value):
        response = order_api_client.get_orders(limit=10, page=page_value)
        response_json = assert_orders_response_success(response)

        assert response_json["pageInfo"]["page"] == page_value


    @allure.title("10 заказов с courierId, limit и page")
    @allure.description("Проверка пагинации с фильтром по courierId")
    def test_get_orders_with_courier_limit_page_returns_200(self, order_api_client, valid_courier_id):
        response = order_api_client.get_orders(courier_id=valid_courier_id, limit=10, page=0)
        response_json = assert_orders_response_success(response)

        assert len(response_json["orders"]) <= 10
        assert response_json["pageInfo"]["limit"] == 10
        assert response_json["pageInfo"]["page"] == 0


    @allure.title('10 заказов возле станции "Калужская" (110)')
    @allure.description("Проверка фильтрации по nearestStation")
    def test_get_orders_near_kaluzhskaya_station_returns_200(self, order_api_client, valid_courier_id):
        response = order_api_client.get_orders(
            courier_id=valid_courier_id,
            limit=10,
            page=0,
            nearest_station='["110"]',
        )
        response_json = assert_orders_response_success(response)

        assert len(response_json["orders"]) <= 10


    @allure.title("Проверка структуры availableStations")
    @allure.description("Проверка полей name, number, color у станции")
    def test_get_orders_available_stations_has_required_fields(self, order_api_client):
        response = order_api_client.get_orders(limit=10, page=0)
        response_json = assert_orders_response_success(response)
        stations = response_json["availableStations"]

        assert len(stations) > 0
        assert_available_station_structure(stations[0])


    @allure.title("Комплексный запрос: все параметры вместе")
    @allure.description("Проверка courierId, nearestStation, limit и page")
    def test_get_orders_all_params_returns_200(self, order_api_client, valid_courier_id):
        response = order_api_client.get_orders(
            courier_id=valid_courier_id,
            nearest_station='["1", "2"]',
            limit=15,
            page=0,
        )
        response_json = assert_orders_response_success(response)

        assert len(response_json["orders"]) <= 15
        assert response_json["pageInfo"]["limit"] == 15
        assert response_json["pageInfo"]["page"] == 0
