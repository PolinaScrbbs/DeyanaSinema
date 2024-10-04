from fastapi import HTTPException, status
from sqlalchemy.sql import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Reservation


async def reservation_exists_by_ticket(session: AsyncSession, ticket_id: int) -> None:
    result = await session.execute(
        select(exists().where(Reservation.ticket_id == ticket_id))
    )
    reservation_exists = result.scalar()

    if reservation_exists:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Билет уже забронирован")
