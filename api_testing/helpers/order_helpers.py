import datetime


def generate_order_payload():
    return {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
        "comment": "Saske, come back to Konoha"
    }
