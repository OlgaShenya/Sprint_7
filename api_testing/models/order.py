class Order:
    def __init__(self, firstName, lastName, address, metroStation, 
                 phone, rentTime, deliveryDate, comment, color=None):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.metroStation = metroStation
        self.phone = phone
        self.rentTime = rentTime
        self.deliveryDate = deliveryDate
        self.comment = comment
        self.color = color

    def to_dict(self):
        data = {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "address": self.address,
            "metroStation": self.metroStation,
            "phone": self.phone,
            "rentTime": self.rentTime,
            "deliveryDate": self.deliveryDate,
            "comment": self.comment
        }
        # Добавляем color только если он не None
        if self.color is not None:
            data["color"] = self.color
        return data