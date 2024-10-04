from typing import List
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..ticket.utils import ticket_exists_by_id
from ..user.models import User, Role
from ..user.utils import user_exists_by_id

from .models import Reservation
from .schemes import ReservationCreate
from .utils import reservation_exists_by_ticket


async def create_reservation(
    session: AsyncSession, reservation_data: ReservationCreate, cashier_id: int
) -> Reservation:
    await reservation_exists_by_ticket(session, reservation_data.ticket_id)
    await ticket_exists_by_id(session, reservation_data.ticket_id)
    await user_exists_by_id(session, reservation_data.booked_user_id)
    await user_exists_by_id(session, cashier_id, "Кассир не найден")

    result = await session.execute(
        select(User.role).where(User.id == reservation_data.booked_user_id)
    )
    booked_user_role = result.scalar()
    print(f"Booked user role: {booked_user_role}, Expected: {Role.CASHIER}")
    if booked_user_role == Role.CASHIER:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Вы не можете сделать бронь на кассира"
        )

    new_reservation = Reservation(
        ticket_id=reservation_data.ticket_id,
        booked_user_id=reservation_data.booked_user_id,
        cashier_id=cashier_id,
    )

    session.add(new_reservation)
    await session.commit()
    await session.refresh(new_reservation)

    return new_reservation
