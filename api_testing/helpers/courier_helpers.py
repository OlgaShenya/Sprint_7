import uuid


def generate_courier_payload():
    return {
        "login": "courier_" + uuid.uuid4().hex[:8],
        "password": "AutoTest123!",
        "firstName": "QA_Student"
    }
