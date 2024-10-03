from fastapi import HTTPException, status
from sqlalchemy.sql import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Session


async def session_exists_by_id(session: AsyncSession, session_id: int) -> None:
    result = await session.execute(select(exists().where(Session.id == session_id)))
    user_exists = result.scalar()

    if not user_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Сессия не найдена")
