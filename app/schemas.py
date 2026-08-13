from datetime import datetime

from pydantic import BaseModel


class TicketPDFRequest(BaseModel):
    ticket_id: int

    passenger_name: str

    flight_number: str

    departure_country: str
    departure_airport: str

    arrival_country: str
    arrival_airport: str

    departure_time: datetime
    arrival_time: datetime

    seat_number: int

    airline: str