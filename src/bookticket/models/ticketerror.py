class TicketError(Exception):
    def __init__(self, message):
        super().__init__(message)


class BusAlreadyDepartedError(TicketError):
    def __init__(self, message):
        super().__init__(message)


class NoAvailableSeatsError(TicketError):
    def __init__(self, message):
        super().__init__(message)


class InvalidRouteIdError(ValueError):
    def __init__(self, message):
        super().__init__(message)


    # def __init__(self, message):
    #     self.message = message


# Створити власне виключення TicketError
# Переробити код таким чином, щоб при спробі купити квиток на рейс, який уже відправився або на який відсутні вільні квитки, генерувалося це виключення.
# Виключеня має генеруватися із різними повідомленнями. Повернути користувачу це повідомлення