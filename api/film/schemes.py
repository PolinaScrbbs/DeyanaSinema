from pydantic import BaseModel, Field
from typing import List, Optional, Union

from .models import Genre, AgeRating


class GenreCreate(BaseModel):
    title: str = Field(..., title="Название жанра", max_length=30)


class GenreResponse(BaseModel):
    id: int
    title: str


class FilmCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=30)
    description: str = Field(..., max_length=200)
    age_rating: AgeRating = AgeRating.PG_13
    duration: int = Field(..., ge=120, description="Duration in minutes")
    release_year: int = Field(..., ge=1888, description="Year of film release")
    genre_ids: List[int]


class FilmResponse(BaseModel):
    id: int
    title: str
    description: str
    age_rating: Union[AgeRating, str]
    duration: int
    release_year: int
    genres: Optional[List[str]] = []
