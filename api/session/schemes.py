from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..film.schemes import FilmResponse
from ..ticket.models import TicketRow, Place


class SessionCreate(BaseModel):
    film_id: int
    start_time: Optional[datetime] = None


class SessionUpdate(BaseModel):
    film_id: Optional[int] = None
    start_time: Optional[datetime] = None


class SessionResponse(BaseModel):
    id: int
    film: FilmResponse
    start_time: datetime


class TicketResponse(BaseModel):
    basic_price: float
    room_number: int
    row_number: TicketRow
    place: Place
    session: SessionResponse


class SessionResponseWithTickets(SessionResponse):
    tickets: List[TicketResponse]
