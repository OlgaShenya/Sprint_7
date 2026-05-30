import datetime
import pytest
import uuid
from api_testing.models.courier import Courier
from api_testing.api.courier_client import CourierAPI
from api_testing.methods.courier_methods import register_new_courier_and_return_login_password
from api_testing.models.order import Order
from api_testing.api.order_client import OrderAPI
from urls import BASE_URL

@pytest.fixture
def api_client():
    client = CourierAPI(BASE_URL)
    created_courier_ids = []
    original_create = client.create

    def create(payload):
        response = original_create(payload)
        if response.status_code == 201:
            login_resp = client.login(payload)
            if login_resp.status_code == 200:
                created_courier_ids.append(login_resp.json()["id"])
        return response

    client.create = create
    yield client
    for courier_id in created_courier_ids:
        client.delete(courier_id)

@pytest.fixture
def valid_courier():
    return Courier(
        login="courier_" + uuid.uuid4().hex[:8],
        password="AutoTest123!",
        firstName="QA_Student"
    )

@pytest.fixture
def valid_payload(valid_courier):
    return valid_courier.to_dict()

@pytest.fixture
def created_courier_payload(api_client):
    login, password, first_name = register_new_courier_and_return_login_password(client=api_client)
    return {"login": login, "password": password, "firstName": first_name}

@pytest.fixture
def valid_courier_id(api_client):
    creds = register_new_courier_and_return_login_password(client=api_client)
    login, password, _ = creds
    login_resp = api_client.login({"login": login, "password": password})
    return login_resp.json()["id"]

@pytest.fixture
def order_api_client():
    return OrderAPI(BASE_URL)

@pytest.fixture
def valid_order_payload():
    return Order(
        firstName="Naruto",
        lastName="Uchiha",
        address="Konoha, 142 apt.",
        metroStation=4,
        phone="+7 800 355 35 35",
        rentTime=5,
        deliveryDate=(datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
        comment="Saske, come back to Konoha"
    ).to_dict()
