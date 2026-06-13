import uuid
from api_testing.api.order_client import OrderAPI


def create_order(base_url, payload=None):
    client = OrderAPI(base_url)
    if payload is None:
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test Address",
            "metroStation": 1,
            "phone": "+7 999 999 99 99",
            "rentTime": 1,
            "deliveryDate": "2025-01-01",
            "comment": "Auto-created order",
        }
    return client.create(payload)


def get_orders(base_url, **kwargs):
    client = OrderAPI(base_url)
    return client.get_orders(
        courier_id=kwargs.get("courier_id"),
        nearest_station=kwargs.get("nearest_station"),
        limit=kwargs.get("limit"),
        page=kwargs.get("page"),
    )
