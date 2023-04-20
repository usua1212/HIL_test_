import uuid
from bookticket.models.bus import Bus
from bookticket.models.route import Route


class Ticket:
    def __init__(self, idt, route_id, seat_number, ticket_number):
        self.id = idt
        self.route_id = route_id
        self.seat_number = seat_number
        self.ticket_number = ticket_number

    def __str__(self):
        return f"Ticket(id={self.id}, route_id={self.route_id}, seat_number={self.seat_number}, ticket_number={self.ticket_number})"
