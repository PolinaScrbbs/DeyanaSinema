from typing import List, Optional, Union
from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user.utils import cashier_check

from .schemes import GenreCreate, GenreResponse, FilmCreate, FilmUpdate, FilmResponse
from . import queries as qr
from . import validators as validator

router = APIRouter(prefix="/films")


################################################################################
#_____________________________________GENRE___________________________________#
##############################################################################


@router.post(
    "/genres/", response_model=GenreResponse, status_code=status.HTTP_201_CREATED
)
async def create_genre(
    genre_create: GenreCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await cashier_check(current_user)
    return await qr.create_genre(session, genre_create)


@router.get("/genres/", response_model=Union[List[GenreResponse], GenreResponse])
async def get_genres_or_genre(
    title: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user)
):
    if not title:
        genres = await qr.get_all_genres(session)
        return genres

    genre = await qr.get_genre_by_title(session, title)
    return genre


@router.get("/genres/{genre_id}", response_model=GenreResponse)
async def get_genre_by_id(
    genre_id: int,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user)
):
    genre = await qr.get_genre_by_id(session, genre_id)
    return genre


@router.put("/genres/{genre_id}", response_model=GenreResponse)
async def update_genre(
    genre_id: int,
    genre_update: GenreCreate,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user)
):
    updated_genre = await qr.update_genre(session, genre_id, genre_update)
    return updated_genre


@router.delete("/genres/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(
    genre_id: int,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user)
):
    await qr.delete_genre(session, genre_id)
    return None


################################################################################
#_____________________________________FILM____________________________________#
##############################################################################


@router.post("/", response_model=FilmResponse, status_code=status.HTTP_201_CREATED)
async def create_film(
    film_create: FilmCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await cashier_check(current_user)
    created_film = await qr.create_film(session, film_create)
    return await validator.film_to_dydantic(created_film)


@router.get("/", response_model=Union[List[FilmResponse], FilmResponse])
async def get_films_or_film(
    title: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user)
):
    if not title:
        films = await qr.get_all_films(session)
        return await validator.list_films_to_dypdantic(films)

    film = await qr.get_film_by_title(session, title)
    return await validator.film_to_dydantic(film)


@router.get("/{film_id}", response_model=FilmResponse)
async def get_film_by_id(
    film_id: int,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user)
):
    film = await qr.get_film_by_id(session, film_id)
    return await validator.film_to_dydantic(film)


@router.patch("/films/{film_id}")
async def update_film(
    film_id: int,
    film_update: FilmUpdate,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user)
):
    updated_film = await qr.update_film(session, film_id, film_update)
    return await validator.film_to_dydantic(updated_film)


@router.delete("/{film_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_film(
    film_id: int,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user)
):
    await qr.delete_film(session, film_id)
    return None
