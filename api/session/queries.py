from typing import List
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..film.utils import existing_film_by_id
from .models import Session
from .schemes import SessionCreate, SessionUpdate


async def create_session(
    session: AsyncSession, session_create: SessionCreate
) -> Session:
    await existing_film_by_id(session, session_create.film_id)

    new_session = Session(
        film_id=session_create.film_id, start_time=session_create.start_time
    )

    session.add(new_session)
    await session.commit()
    await session.refresh(new_session)

    return new_session


async def get_all_sessions(session: AsyncSession) -> List[Session]:
    result = await session.execute(select(Session))

    film_sessions = result.scalars().all()
    if not film_sessions:
        raise HTTPException(status.HTTP_204_NO_CONTENT, "Список сеансов пуст")

    return film_sessions


async def get_session_by_id(session: AsyncSession, session_id: int) -> Session:
    result = await session.execute(select(Session).where(Session.id == session_id))

    film_session = result.scalar_one_or_none()
    if not film_session:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Сеанс не найден")

    return film_session


async def update_session(
    async_session: AsyncSession, session_id: int, session_update: SessionUpdate
) -> Session:
    session = await get_session_by_id(async_session, session_id)

    if session_update.film_id is not None:
        session.film_id = session_update.film_id
    if session_update.start_time is not None:
        session.start_time = session_update.start_time

    async_session.add(session)
    await async_session.commit()
    await async_session.refresh(session)

    return session


async def delete_session(async_session: AsyncSession, session_id: int) -> None:
    session = await async_session.get(Session, session_id)
    if not session:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Фильм не найден.")

    await async_session.delete(session)
    await async_session.commit()
