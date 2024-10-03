from typing import List
from .models import Film
from .schemes import FilmResponse


async def film_to_pydantic(film: Film) -> FilmResponse:
    return FilmResponse(
        id=film.id,
        title=film.title,
        description=film.description,
        age_rating=film.age_rating,
        duration=film.duration,
        release_year=film.release_year,
        genres=[genre.title for genre in film.genres],
    )


async def list_film_to_pydantic(films: List[Film]) -> List[FilmResponse]:
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
