from typing import List, Optional, Union
from annotated_types import Ge
from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user.utils import cashier_check

from .schemes import GenreCreate, GenreResponse, FilmCreate, FilmResponse
from . import queries as qr

router = APIRouter(prefix="/films")


################################################################################
# ____________________________________GENRE____________________________________#
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


################################################################################
# ____________________________________FILM_____________________________________#
##############################################################################


@router.post("/", response_model=FilmResponse, status_code=status.HTTP_201_CREATED)
async def create_film(
    film_create: FilmCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await cashier_check(current_user)
    created_film = await qr.create_film(session, film_create)
    return created_film


@router.get("/films/", response_model=Union[List[FilmResponse], FilmResponse])
async def get_films_or_film(
    title: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user)
):
    if not title:
        films = await qr.get_all_films(session)
        return films

    film = await qr.get_film_by_title(session, title)
    return film


@router.get("/{film_id}", response_model=FilmResponse)
async def get_film_by_id(
    film_id: int,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user)
):
    film = await qr.get_film_by_id(session, film_id)
    return film
