class Contact:
    def __init__(self, first_name, last_name, phone_number, address="", date_of_birth=""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.date_of_birth = date_of_birth

    def __str__(self):
        return f"Contact {self.first_name}, {self.last_name}, {self.phone_number}, {self.address}, {self.date_of_birth}"
