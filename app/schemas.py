from datetime import datetime

from pydantic import BaseModel


class TicketPDFRequest(BaseModel):
    ticket_id: int

    passenger_name: str

    flight_number: str

    departure_code: str
    departure_city: str

    arrival_code: str
    arrival_city: str

    departure_time: datetime
    arrival_time: datetime

    seat_number: int

    airline: str