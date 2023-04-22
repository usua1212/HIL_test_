
class TicketError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        if not self.routes[route_id].departure_time > current_date:
            print("Sorry, there are no seats available on this bus")
            return
