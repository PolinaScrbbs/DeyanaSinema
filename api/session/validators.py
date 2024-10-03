from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from ..film.queries import get_film_by_id
from ..film.validators import film_to_pydantic

from .models import Session
from .schemes import SessionResponse


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
