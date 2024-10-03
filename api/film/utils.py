from fastapi import HTTPException, status
from sqlalchemy.sql import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Film


async def existing_film_by_title(session: AsyncSession, title: str) -> bool:
    result = await session.execute(select(exists().where(Film.title == title)))
    return result.scalar()


async def existing_film_by_id(session: AsyncSession, id: int) -> None:
    result = await session.execute(select(exists().where(Film.id == id)))
    film_exists = result.scalar()
    if not film_exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Фильм не найден")
