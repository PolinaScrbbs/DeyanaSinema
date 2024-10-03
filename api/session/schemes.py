from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from ..film.schemes import FilmResponse


class SessionCreate(BaseModel):
    film_id: int
    start_time: Optional[datetime] = None


class SessionUpdate(BaseModel):
    film_id: Optional[int] = None
    start_time: Optional[datetime] = None


class SessionResponse(BaseModel):
    id: int
    film: FilmResponse
    start_time: datetime
