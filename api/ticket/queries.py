from typing import List
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..session.utils import session_exists_by_id

from .models import Ticket, RoomNumber
from .schemes import TicketCreate, UpdateTicket


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


async def get_all_tikcets(session: AsyncSession) -> List[Ticket]:
    result = await session.execute(select(Ticket))
    tickets = result.scalars().all()
    if not tickets:
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    return tickets


async def get_ticket_by_id(session: AsyncSession, tikcet_id: int) -> Ticket:
    result = await session.execute(select(Ticket).where(Ticket.id == tikcet_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Билет не найден")
    return ticket


async def update_ticket(
    session: AsyncSession, ticket_id: int, ticket_data: UpdateTicket
) -> Ticket:
    ticket = await get_ticket_by_id(session, ticket_id)

    if ticket_data.basic_price is not None:
        ticket.basic_price = ticket_data.basic_price
    if ticket_data.room_number is not None:
        ticket.room_number = ticket_data.room_number
    if ticket_data.row_number is not None:
        ticket.row_number = ticket_data.row_number
    if ticket_data.place is not None:
        ticket.place = ticket_data.place

    await session.commit()
    await session.refresh(ticket)

    return ticket


async def delete_ticket(session: AsyncSession, ticket_id: int) -> None:
    ticket = await session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    await session.delete(ticket)
    await session.commit()
