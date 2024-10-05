from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from api.ticket.models import Ticket

from ..film.queries import get_film_by_id
from ..film.validators import film_to_pydantic

from .models import Session
from .schemes import SessionResponse, TicketResponse


async def session_to_pydantic(
    async_session: AsyncSession, session: Session
) -> SessionResponse:
    session_film = await get_film_by_id(async_session, session.film_id)
    pydantic_session_film = await film_to_pydantic(session_film)
    return SessionResponse(
        id=session.id, film=pydantic_session_film, start_time=session.start_time
    )


async def list_sessions_to_pydantic(
    async_session: AsyncSession, sessions: List[Session]
) -> List[SessionResponse]:
    pydantic_sessions = []

    for session in sessions:
        session_film = await get_film_by_id(async_session, session.film_id)
        pydantic_session_film = await film_to_pydantic(session_film)

        pydantic_sessions.append(
            SessionResponse(
                id=session.id, film=pydantic_session_film, start_time=session.start_time
            )
        )

    return pydantic_sessions


async def ticket_to_pydantic(session: AsyncSession, ticket: Ticket) -> TicketResponse:
    return TicketResponse(
        id=ticket.id,
        basic_price=ticket.basic_price,
        room_number=await ticket.room_number.number,
        row_number=ticket.row_number,
        place=ticket.place,
    )


async def list_tickets_to_pydantic(
    session: AsyncSession, tickets: List[Ticket]
) -> List[TicketResponse]:
    ticket_responses = []
    for ticket in tickets:
        ticket_response = await ticket_to_pydantic(session, ticket)
        ticket_responses.append(ticket_response)

    return ticket_responses
