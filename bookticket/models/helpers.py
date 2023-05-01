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
        self.buses = self.get_buses_from_file('data\\bus.csv')
        self.routes = self.get_routes_from_file('data\\route.csv')
        self.tickets = self.get_tickets_from_file('data\\ticket.csv')

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
                bus = next((b for b in self.buses if b.id == bus_id), None)
                route = Route(idr, days, hours, minutes, destination, bus)
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

    def save_tickets_to_file(self, tickets):
        with open('data\\ticket.csv', mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for ticket in tickets:
                writer.writerow([ticket.id, ticket.route_id, ticket.seat_number, ticket.ticket_number])

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
            if item.departure_time.ctime().startswith(weekday.title()) and item.destination.lower().startswith(city.lower())
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
        self.save_tickets_to_file([ticket])
        print("The tickets are booked:", ticket)

    def book_multiple_seats(self, route_id, num_seat, max_seats, avail_seats):
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
            ticket_ids = []
            for seat in adjacent_seats:
                ticket_id = str(uuid.uuid4())
                ticket_ids.append(ticket_id)
                ticket = Ticket(len(self.tickets), route_id, seat, ticket_id)
                self.tickets.append(ticket)
            self.save_tickets_to_file(self.tickets[-num_seat:])
            ticket_strings = [str(ticket) for ticket in self.tickets[-num_seat:]]
            print("The tickets are booked:", ", ".join(ticket_strings))
        else:
            print("There are not enough adjacent seats available")

    def add_bus(self):
        # Get inputs for model, car_number, and max_seats from user
        model = input("Enter bus model: ")
        car_number = input("Enter car number: ")
        max_seats = int(input("Enter maximum number of seats: "))
        # Generate id for new bus by getting the last bus id and adding 1
        idb = self.buses[-1].id + 1
        # Create a new Bus instance with the input values and id
        bus = Bus(idb, model, car_number, max_seats)
        # Append the new bus to the list of buses
        self.buses.append(bus)
        # Write the new list of buses to the bus.csv file
        with open("data\\bus.csv", mode="a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([bus.id, bus.model, bus.car_number, bus.max_seats])
        print(f"New bus added to file with id {bus.id}.")

    def add_route(self):
        # Get inputs for days, hours, minutes, destination, and bus id from user
        days = int(input("Enter days (0-6): "))
        hours = int(input("Enter departure hours (0-23): "))
        minutes = int(input("Enter departure minutes (0-59): "))
        destination = input("Enter destination: ")
        bus_id = int(input("Enter bus id: "))
        # Generate id for new route by getting the last route id and adding 1
        idr = self.routes[-1].id + 1
        # Get the bus instance with the given bus id
        bus = next((b for b in self.buses if b.id == bus_id), None)
        # If the bus with the given id is not found, exit the function
        if not bus:
            print(f"No bus found with id {bus_id}.")
            return
        # Create a new Route instance with the input values and id
        route = Route(idr, days, hours, minutes, destination, bus)
        # Append the new route to the list of routes
        self.routes.append(route)
        # Write the new list of routes to the route.csv file
        with open("data\\route.csv", mode="a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [route.id, route.departure_time.weekday(), route.departure_time.hour, route.departure_time.minute, route.destination, route.bus.id])
        print(f"New route added to file with id {route.id}.")

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
