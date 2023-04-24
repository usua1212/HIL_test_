from datetime import datetime
from bookticket.models.bus import Bus


class Route:
    def __init__(self, idr, departure_time, destination, bus):
        self.id = idr
        self.departure_time = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)
        self.destination = destination
        self.bus_id = bus_id

    def __str__(self):
        return f"route ID: {self.id}, departure Time: {self.departure_time.strftime('%Y-%m-%d %H:%M')}, destination: {self.destination}, bus ID: {self.bus_id}"

