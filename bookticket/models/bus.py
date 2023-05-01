class Bus:
    def __init__(self, idb, model, car_number, max_seats):
        self.id = idb
        self.model = model
        self.car_number = car_number
        self.max_seats = max_seats

    def __str__(self):
        return f"Bus(id={self.id}, model={self.model}, car_number={self.car_number}, max_seats={self.max_seats})"

