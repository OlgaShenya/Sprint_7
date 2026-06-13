class Courier:
    def __init__(self, login, password, firstName):
        self.login = login
        self.password = password
        self.firstName = firstName

    def to_dict(self):
        return {
            "login": self.login,
            "password": self.password,
            "firstName": self.firstName
        }