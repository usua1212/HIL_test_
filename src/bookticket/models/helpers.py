import uuid
from bookticket.models.bus import Bus
from bookticket.models.route import Route
from bookticket.models.ticket import Ticket
from bookticket.models.ticketerror import TicketError, BusAlreadyDepartedError, NoAvailableSeatsError
from datetime import datetime, timedelta


def wish_decorator(func):
    def wrapper(*args, **kwargs):
        print("Today is", datetime.today().strftime("%Y-%m-%d"))
        result = func(*args, **kwargs)
        print("Have a nice day!")
        return result
    return wrapper


class Controller:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.buses = [
            Bus(0, 'Mercedes-Benz Sprinter', 'AA1234AA', 20),
            Bus(1, 'Neoplan N 1116', 'AA2345AA', 57),
            Bus(2, 'Setra', 'AA3456AA', 30),
            Bus(3, 'MAN', 'AA4567AA', 50)
        ]
        today = datetime.today()
        start = datetime(today.year, today.month, today.day)
        monday_start = start - timedelta(days=today.weekday())
        self.routes = [
                Route(0, monday_start + timedelta(days=0, hours=6, minutes=25), 'Odesa', self.get_bus_by_id(1)),
                Route(1, monday_start + timedelta(days=4, hours=8, minutes=40), 'Poltava', self.get_bus_by_id(1)),
                Route(2, monday_start + timedelta(days=1, hours=14, minutes=15), 'Zhytomyr', self.get_bus_by_id(0)),
                Route(3, monday_start + timedelta(days=2, hours=12, minutes=0), 'Lviv', self.get_bus_by_id(2)),
                Route(4, monday_start + timedelta(days=4, hours=18, minutes=10), 'Kyiv', self.get_bus_by_id(3)),
                Route(5, monday_start + timedelta(days=3, hours=5, minutes=15), 'Chernihiv', self.get_bus_by_id(0)),
                Route(6, monday_start + timedelta(days=5, hours=11, minutes=50), 'Rivne', self.get_bus_by_id(3)),
                Route(7, monday_start + timedelta(days=2, hours=20, minutes=18), 'Kharkiv', self.get_bus_by_id(1)),
                Route(8, monday_start + timedelta(days=4, hours=15, minutes=20), 'Poltava', self.get_bus_by_id(2)),
                Route(9, monday_start + timedelta(days=6, hours=16, minutes=20), 'Ternopil', self.get_bus_by_id(0))
                ]
        self.tickets = [
                Ticket(0, self.routes[0].id, 1, uuid.uuid4()),
                Ticket(1, self.routes[0].id, 2, uuid.uuid4()),
                Ticket(2, self.routes[0].id, 3, uuid.uuid4()),
                Ticket(3, self.routes[1].id, 24, uuid.uuid4()),
                Ticket(4, self.routes[1].id, 1, uuid.uuid4()),
                Ticket(5, self.routes[2].id, 2, uuid.uuid4()),
                Ticket(6, self.routes[2].id, 3, uuid.uuid4()),
                Ticket(7, self.routes[3].id, 22, uuid.uuid4()),
                Ticket(8, self.routes[9].id, 8, uuid.uuid4()),
                Ticket(9, self.routes[9].id, 15, uuid.uuid4())
                ]

    @wish_decorator
    def show_routes(self):
        for item in self.routes:
            print(item)

    def show_free_tickets(self, route_id):
        try:
            route_id = int(route_id)
        except ValueError
        current_date = datetime.now()
        if not self.routes[route_id].departure_time > current_date:
            raise BusAlreadyDepartedError('The departure time of the route has already passed.')
        booked_seats = [ticket.seat_number for ticket in self.tickets if ticket.route_id == route_id]
        print("Tickets have been booked:", booked_seats)
        max_seats = self.routes[route_id].bus.max_seats
        print("Total seats", max_seats)
        avail_seats = set(range(1, max_seats + 1)) - set(booked_seats)
        print("Free places", sorted(avail_seats))
        if not avail_seats:
            raise NoAvailableSeatsError("There are no available tickets left for this route.")
        num_seat = int(input("How many seats do you want to book: "))
        if num_seat == 1:
            self.book_one_seat(route_id, booked_seats)
        elif num_seat > 1:
            self.book_multiple_seats(route_id, num_seat, max_seats, avail_seats)
        elif num_seat == 0:
            print("Enter a number of seats greater than 0.")
            return

    def search_routes(self):
        request = input("Enter the day and direction using the example: fri, poltava: ")
        weekday, city = request.split(", ")
        matched_routes = [
            item
            for item in self.routes
            if item.departure_time.ctime().startswith(weekday.title())
            and item.destination.lower().startswith(city.lower())
        ]
        if not matched_routes:
            print("No routes found")
            return
        print("Matched routes:")
        for route in matched_routes:
            booked_seats = [ticket.seat_number for ticket in self.tickets if ticket.route_id == route.id]
            max_seats = route.bus.max_seats
            avail_seats = set(range(1, max_seats + 1)) - set(booked_seats)
            print(
                f"Route id:{route.id} - departure time: {route.departure_time.ctime()}, destination: {route.destination}, available seats: {sorted(avail_seats)}"
            )
        route_ids = input("Enter the route ID you want to book: ")
        selected_routes = []
        for route in matched_routes:
            if str(route.id) == route_ids:
                selected_routes.append(route)
        if len(selected_routes) == 0:
            print("No valid routes selected")
            return
        for route in selected_routes:
            avail_seats = [ticket.seat_number for ticket in self.tickets if ticket.route_id == route.id]
            max_seats = route.bus.max_seats
            avail_seats = set(range(1, max_seats + 1)) - set(avail_seats)
            print(
                f"Selected route id:{route.id} - departure time: {route.departure_time.ctime()}, destination: {route.destination}, available seats: {sorted(avail_seats)}"
            )
            num_seat = int(input("How many seats do you want to book: "))
            if num_seat == 1:
                self.book_one_seat(route.id, booked_seats)
            elif num_seat > 1:
                self.book_multiple_seats(route.id, num_seat, max_seats, avail_seats)
            elif num_seat == 0:
                print("Enter a number of seats greater than 0.")
                return

    def book_one_seat(self, route_id, booked_seats):
        seat_num = int(input("Enter the seat number you want to book: "))
        if seat_num in booked_seats:
            print("Sorry, this seat has already been booked")
            return
        ticket_idf = uuid.uuid4()
        ticket = Ticket(len(self.tickets), route_id, seat_num, ticket_idf)
        self.tickets.append(ticket)
        print("The tickets are booked:", ticket)

    def book_multiple_seats(self, route_id, num_seat, max_seats, avail_seats):
        # чи достатньо вільних сусідніх місць
        adjacent_seats = []
        for seat in range(1, max_seats + 1):
            if seat in avail_seats:
                if not adjacent_seats:
                    adjacent_seats.append(seat)
                elif seat == adjacent_seats[-1] + 1:
                    adjacent_seats.append(seat)
                    if len(adjacent_seats) == num_seat:
                        break
                else:
                    adjacent_seats = [seat]
        if len(adjacent_seats) == num_seat:
            # Бронювання місць поруч
            ticket_ids = []
            for seat in adjacent_seats:
                ticket_id = uuid.uuid4()
                ticket_ids.append(ticket_id)
                ticket = Ticket(self.tickets, route_id, seat, ticket_id)
                self.tickets.append(ticket)
            ticket_strings = [ticket for ticket in self.tickets[-num_seat:]]
            print("The tickets are booked:", ticket_strings)
        else:
            print("There are not enough adjacent seats available")

    def get_bus_by_id(self, bus_id):
        for bus in self.buses:
            if bus.id == bus_id:
                return bus
        return None

    def get_route_by_id(self, route_id):
        for route in self.routes:
            if route.id == route_id:
                return route
        return None

    def get_ticket_by_id(self, ticket_id):
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                return ticket
        return None

