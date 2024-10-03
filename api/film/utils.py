from sqlalchemy.sql import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Film


async def existing_film_by_title(session: AsyncSession, title: str) -> bool:
    result = await session.execute(select(exists().where(Film.title == title)))
    return result.scalar()
