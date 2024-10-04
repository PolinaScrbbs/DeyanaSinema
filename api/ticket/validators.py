from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from ..session.queries import get_session_by_id
from ..session.validators import session_to_pydantic

from .models import Ticket
from .schemes import TicketResponse


async def ticket_to_pydantic(session: AsyncSession, ticket: Ticket) -> TicketResponse:
    ticket_session = await get_session_by_id(session, ticket.session_id)
    pydantic_ticket_session = await session_to_pydantic(session, ticket_session)

    return TicketResponse(
        basic_price=ticket.basic_price,
        room_number=await ticket.room_number.number,
        row_number=ticket.row_number,
        place=ticket.place,
        session=pydantic_ticket_session,
    )


async def list_tickets_to_pydantic(
    session: AsyncSession, tickets: List[Ticket]
) -> List[TicketResponse]:
    ticket_responses = []
    for ticket in tickets:
        ticket_response = await ticket_to_pydantic(session, ticket)
        ticket_responses.append(ticket_response)

    return ticket_responses
