class TicketError(Exception):
    def __init__(self, message):
        super().__init__(message)


class BusAlreadyDepartedError(TicketError):
    def __init__(self, message):
        super().__init__(message)


class NoAvailableSeatsError(TicketError):
    def __init__(self, message):
        super().__init__(message)
