from bookticket.models.helpers import Controller


class TicketError(Exception):
    def __init__(self, message):
        self.message = message

try:
    if not self.routes[route_id].departure_time > current_date:
        raise TicketError("Sorry, there are no seats available on this bus")
try:
    if not avail_seats:
        raise TicketError("Sorry, there are no seats available on this bus")
try:
    if seat_num in booked_seats:
        raise TicketError("Sorry, this seat has already been booked")









