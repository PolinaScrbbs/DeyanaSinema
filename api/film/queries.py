from typing import List
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Film, Genre
from .schemes import GenreCreate, GenreResponse, FilmCreate, FilmUpdate
from .utils import existing_film_by_title


################################################################################
# _____________________________________GENRE___________________________________#
##############################################################################


async def create_genre(
    session: AsyncSession, genre_create: GenreCreate
) -> GenreResponse:
    existing_genre = await session.execute(
        select(Genre).where(Genre.title == genre_create.title)
    )

    if existing_genre.scalar() is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Жанр с таким названием уже существует",
        )

    new_genre = Genre(title=genre_create.title)
    session.add(new_genre)
    await session.commit()
    await session.refresh(new_genre)

    return GenreResponse(id=new_genre.id, title=new_genre.title)


async def get_all_genres(session: AsyncSession) -> List[Genre]:
    result = await session.execute(select(Genre))
    genres = result.scalars().all()
    if not genres:
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    return genres


async def get_genre_by_id(session: AsyncSession, genre_id: int) -> Genre:
    result = await session.execute(select(Genre).where(Genre.id == genre_id))
    genre = result.scalar_one_or_none()
    if not genre:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Жанр не найден")
    return genre


async def get_genre_by_title(session: AsyncSession, genre_title: str) -> Genre:
    result = await session.execute(select(Genre).where(Genre.title == genre_title))
    genre = result.scalar_one_or_none()
    if not genre:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Жанр не найден")
    return genre


async def update_genre(
    session: AsyncSession, genre_id: int, genre_update: GenreCreate
) -> Genre:
    genre = await get_genre_by_id(session, genre_id)
    if not genre:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Жанр не найден")

    genre.title = genre_update.title
    await session.commit()
    await session.refresh(genre)

    return genre


async def delete_genre(session: AsyncSession, genre_id: int) -> None:
    genre = await session.get(Genre, genre_id)
    if not genre:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Жанр не найден")

    await session.delete(genre)
    await session.commit()


################################################################################
# _____________________________________FILM____________________________________#
##############################################################################


async def create_film(session: AsyncSession, film_create: FilmCreate) -> Film:
    existing_film = await existing_film_by_title(session, film_create.title)

    if existing_film:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Фильм с таким названием уже существует"
        )

    new_film = Film(
        title=film_create.title,
        description=film_create.description,
        age_rating=film_create.age_rating,
        duration=film_create.duration,
        release_year=film_create.release_year,
    )

    genres = await session.execute(
        select(Genre).where(Genre.id.in_(film_create.genre_ids))
    )
    genre_list = genres.scalars().all()

    if len(genre_list) != len(film_create.genre_ids):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Один или несколько жанров не найдены",
        )

    new_film.genres.extend(genre_list)
    session.add(new_film)
    await session.commit()

    return new_film


async def get_all_films(session: AsyncSession) -> List[Film]:
    result = await session.execute(select(Film).options(selectinload(Film.genres)))
    films = result.scalars().all()
    if not films:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return films


async def get_film_by_id(session: AsyncSession, film_id: int) -> Film:
    result = await session.execute(
        select(Film).where(Film.id == film_id).options(selectinload(Film.genres))
    )
    film = result.scalar_one_or_none()
    if not film:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Фильм не найден")
    return film


async def get_film_by_title(session: AsyncSession, film_title: str) -> Film:
    result = await session.execute(
        select(Film).where(Film.title == film_title).options(selectinload(Film.genres))
    )
    film = result.scalar_one_or_none()
    if not film:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Фильм не найден")
    return film


async def update_film(
    session: AsyncSession, film_id: int, film_update: FilmUpdate
) -> Film:
    film = await get_film_by_id(session, film_id)
    if not film:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Фильм не найден")

    if film_update.title is not None:
        film.title = film_update.title
    if film_update.description is not None:
        film.description = film_update.description
    if film_update.age_rating is not None:
        film.age_rating = film_update.age_rating
    if film_update.duration is not None:
        film.duration = film_update.duration
    if film_update.release_year is not None:
        film.release_year = film_update.release_year

    if film_update.genre_ids is not None:
        genres = await session.execute(
            select(Genre).where(Genre.id.in_(film_update.genre_ids))
        )
        genre_list = genres.scalars().all()

        if len(genre_list) != len(film_update.genre_ids):
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "Один или несколько жанров не найдены"
            )

        film.genres.clear()
        film.genres.extend(genre_list)

    await session.commit()
    await session.refresh(film)

    print(film.age_rating)

    return film


async def delete_film(session: AsyncSession, film_id: int) -> None:
    film = await session.get(Film, film_id)
    if not film:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Фильм не найден")

    await session.delete(film)
    await session.commit()
