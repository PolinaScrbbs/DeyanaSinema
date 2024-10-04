from sqlalchemy.ext.asyncio import AsyncSession

from ..ticket.queries import get_ticket_by_id
from ..user.queries import get_user_by_id
from ..ticket.validators import ticket_to_pydantic
from ..user.validators import user_to_pydantic

from .models import Reservation
from .schemes import ReservationResponse


async def reservation_to_pydantic(
    session: AsyncSession, reservation: Reservation
) -> ReservationResponse:

    ticket = await get_ticket_by_id(session, reservation.ticket_id)
    booked_user = await get_user_by_id(session, reservation.booked_user_id)
    cashier = await get_user_by_id(session, reservation.cashier_id)

    pydantic_ticket = await ticket_to_pydantic(session, ticket)
    pydantic_booked_user = await user_to_pydantic(booked_user)
    pydantic_cashier = await user_to_pydantic(cashier)

    return ReservationResponse(
        id=reservation.id,
        ticket=pydantic_ticket,
        price=await reservation.price,
        booked_user=pydantic_booked_user,
        cashier=pydantic_cashier,
        created_at=reservation.created_at,
    )
