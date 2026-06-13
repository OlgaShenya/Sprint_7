from api_testing.api.courier_client import CourierAPI
import random
import string


def login_courier(base_url, payload):
    client = CourierAPI(base_url)
    return client.login(payload)


def delete_courier(base_url, courier_id):
    client = CourierAPI(base_url)
    return client.delete(courier_id)


def register_new_courier_and_return_login_password(base_url=None, client=None):
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(length))

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    if client is None:
        if base_url is None:
            raise ValueError("Either base_url or client must be provided")
        client = CourierAPI(base_url)

    response = client.create(payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return []
