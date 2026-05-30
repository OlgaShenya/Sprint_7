import allure
import requests


class CourierAPI:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    @allure.step("Создать курьера")
    def create(self, payload):
        url = self.base_url + "/api/v1/courier"
        return self.session.post(url, json=payload, timeout=30)

    @allure.step("Авторизовать курьера")
    def login(self, payload, timeout=30):
        url = self.base_url + "/api/v1/courier/login"
        return self.session.post(url, json=payload, timeout=timeout)

    @allure.step("Удалить курьера")
    def delete(self, courier_id):
        url = self.base_url + f"/api/v1/courier/{courier_id}"
        return self.session.delete(url, timeout=30)
