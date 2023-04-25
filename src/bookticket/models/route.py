from datetime import datetime, timedelta
from bookticket.models.bus import Bus

today = datetime.today()
start = datetime(today.year, today.month, today.day)
monday_start = start - timedelta(days=today.weekday())

class Route:
    def __init__(self, idr, days, hours, minutes, destination, bus):
        self.id = idr
        self.departure_time = monday_start + timedelta(days=days, hours=hours, minutes=minutes)
        self.destination = destination
        self.bus = bus

    def __str__(self):
        return f"route ID: {self.id}, departure Time: {self.departure_time.strftime('%Y-%m-%d %H:%M')}, destination: {self.destination}, bus ID: {self.bus}"
