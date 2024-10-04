from fastapi import HTTPException, status
from sqlalchemy.sql import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Ticket


async def ticket_exists_by_id(session: AsyncSession, ticket_id: int) -> None:
    result = await session.execute(select(exists().where(Ticket.id == ticket_id)))
    user_exists = result.scalar()

    if not user_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Билет не найден")
