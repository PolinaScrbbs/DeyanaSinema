from typing import List
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..session.utils import session_exists_by_id

from .models import Ticket, RoomNumber
from .schemes import TicketCreate


async def create_ticket(session: AsyncSession, ticket_create: TicketCreate) -> Ticket:
    await session_exists_by_id(session, ticket_create.session_id)

    new_ticket = Ticket(
        session_id=ticket_create.session_id,
        basic_price=ticket_create.basic_price,
        room_number=RoomNumber.from_str(ticket_create.room_number),
        row_number=ticket_create.row_number,
        place=ticket_create.place,
    )

    session.add(new_ticket)
    await session.commit()
    await session.refresh(new_ticket)

    return new_ticket
