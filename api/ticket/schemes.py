from pydantic import BaseModel

from ..session.schemes import SessionResponse

from .models import RoomNumber, TicketRow, Place


class TicketCreate(BaseModel):
    session_id: int
    basic_price: float
    room_number: str = "ROOM_1"
    row_number: TicketRow
    place: Place


class TicketResponse(BaseModel):
    basic_price: float
    room_number: int
    row_number: TicketRow
    place: Place
    session: SessionResponse
