class TicketError(Exception):
    def __init__(self, message):
        self.message = message
try:
    if flight.departure_time < datetime.now():
        raise FlightDepartedError("This flight has already departed.")
    elif not flight.has_available_tickets():
        raise NoTicketsAvailableError("Sorry, no tickets available for this flight.")
    else:
        pass
except FlightTicketError as e:
    print(e.message)