import csv
import uuid
from bookticket.models.bus import Bus
from bookticket.models.route import Route
from bookticket.models.ticket import Ticket
from bookticket.models.ticketerror import BusAlreadyDepartedError, NoAvailableSeatsError
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
        self.buses = self.get_buses_from_file('bookticket/data/bus.csv')
        self.routes = self.get_routes_from_file('bookticket/data/route.csv')
        self.tickets = self.get_tickets_from_file('bookticket/data/ticket.csv')

    def get_buses_from_file(self, filename):
        buses = []
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                idb = int(row['idb'])
                model = row['model']
                car_number = row['car_number']
                max_seats = int(row['max_seats'])
                bus = Bus(idb, model, car_number, max_seats)
                buses.append(bus)
        return buses

    def get_routes_from_file(self, filename):
        routes = []
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                idr = int(row['idr'])
                days = int(row['days'])
                hours = int(row['hours'])
                minutes = int(row['minutes'])
                destination = row['destination']
                bus_id = int(row['bus'])
                route = Route(idr, days, hours, minutes, destination, bus_id)
                routes.append(route)
        return routes

    def get_tickets_from_file(self, filename):
        tickets = []
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                idt = int(row['idt'])
                route_id = int(row['route_id'])
                seat_number = int(row['seat_number'])
                ticket_number = row['ticket_number']
                ticket = Ticket(idt, route_id, seat_number, ticket_number)
                tickets.append(ticket)
        return tickets

    @wish_decorator
    def show_routes(self):
        for item in self.routes:
            print(item)

    def show_free_tickets(self, route_id):
        try:
            route_id = int(route_id)
        except ValueError:
            raise ValueError('Invalid route ID')
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
        try:
            num_seat = int(input("How many seats do you want to book: "))
        except ValueError:
            raise ValueError('Invalid number of seats entered.')
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
            raise NoAvailableSeatsError("There are no available tickets left for this route.")
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

