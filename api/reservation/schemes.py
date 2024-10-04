from datetime import datetime
from pydantic import BaseModel

from ..ticket.schemes import TicketResponse
from ..user.schemes import BaseUser


class ReservationCreate(BaseModel):
    ticket_id: int
    booked_user_id: int


class ReservationResponse(BaseModel):
    id: int
    ticket: TicketResponse
    price: float
    booked_user: BaseUser
    cashier: BaseUser
    created_at: datetime
