from typing import List
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Film, Genre
from .schemes import GenreCreate, GenreResponse, FilmCreate, FilmResponse
from .utils import existing_film_by_title


################################################################################
# ____________________________________GENRE____________________________________#
##############################################################################


async def create_genre(
    session: AsyncSession, genre_create: GenreCreate
) -> GenreResponse:
    existing_genre = await session.execute(
        select(Genre).where(Genre.title == genre_create.title)
    )

    if existing_genre.scalar() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Жанр с таким названием уже существует.",
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
        raise HTTPException(status_code=404, detail="Жанры не найдены.")
    return genres


async def get_genre_by_id(session: AsyncSession, genre_id: int) -> Genre:
    result = await session.execute(select(Genre).where(Genre.id == genre_id))
    genre = result.scalar_one_or_none()
    if not genre:
        raise HTTPException(status_code=404, detail="Фильм не найден.")
    return genre


async def get_genre_by_title(session: AsyncSession, genre_title: str) -> Genre:
    result = await session.execute(select(Genre).where(Genre.title == genre_title))
    genre = result.scalar_one_or_none()
    if not genre:
        raise HTTPException(status_code=404, detail="Фильм не найден.")
    return genre


################################################################################
# ____________________________________FILM_____________________________________#
##############################################################################


async def create_film(session: AsyncSession, film_create: FilmCreate) -> FilmResponse:
    existing_film = await existing_film_by_title(session, film_create.title)

    if existing_film:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Фильм с таким названием уже существует.",
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Один или несколько жанров не найдены.",
        )

    new_film.genres.extend(genre_list)
    session.add(new_film)
    await session.commit()

    return FilmResponse(
        id=new_film.id,
        title=new_film.title,
        description=new_film.description,
        age_rating=new_film.age_rating,
        duration=new_film.duration,
        release_year=new_film.release_year,
        genres=[genre.title for genre in new_film.genres],
    )


async def get_all_films(session: AsyncSession) -> List[FilmResponse]:
    result = await session.execute(select(Film).options(selectinload(Film.genres)))
    films = result.scalars().all()
    if not films:
        raise HTTPException(status_code=404, detail="Фильмы не найдены.")
    return [
        FilmResponse(
            id=film.id,
            title=film.title,
            description=film.description,
            age_rating=film.age_rating,
            duration=film.duration,
            release_year=film.release_year,
            genres=[genre.title for genre in film.genres],
        )
        for film in films
    ]


async def get_film_by_id(session: AsyncSession, film_id: int) -> FilmResponse:
    result = await session.execute(
        select(Film).where(Film.id == film_id).options(selectinload(Film.genres))
    )
    film = result.scalar_one_or_none()
    if not film:
        raise HTTPException(status_code=404, detail="Фильм не найден.")
    return FilmResponse(
        id=film.id,
        title=film.title,
        description=film.description,
        age_rating=film.age_rating,
        duration=film.duration,
        release_year=film.release_year,
        genres=[genre.title for genre in film.genres],
    )


async def get_film_by_title(session: AsyncSession, film_title: str) -> FilmResponse:
    result = await session.execute(
        select(Film).where(Film.title == film_title).options(selectinload(Film.genres))
    )
    film = result.scalar_one_or_none()
    if not film:
        raise HTTPException(status_code=404, detail="Фильм не найден.")
    return FilmResponse(
        id=film.id,
        title=film.title,
        description=film.description,
        age_rating=film.age_rating,
        duration=film.duration,
        release_year=film.release_year,
        genres=[genre.title for genre in film.genres],
    )
