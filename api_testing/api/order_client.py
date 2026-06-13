import allure
import requests


class OrderAPI:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    @allure.step("Создать заказ")
    def create(self, payload):
        url = self.base_url + "/api/v1/orders"
        return self.session.post(url, json=payload, timeout=30)

    @allure.step("Получить список заказов")
    def get_orders(self, courier_id=None, nearest_station=None, limit=None, page=None):
        url = self.base_url + "/api/v1/orders"
        params = {}

        if courier_id is not None:
            params["courierId"] = courier_id
        if nearest_station is not None:
            params["nearestStation"] = nearest_station
        if limit is not None:
            params["limit"] = limit
        if page is not None:
            params["page"] = page

        return self.session.get(url, params=params, timeout=30)
