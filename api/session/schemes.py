from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime

from ..film.schemes import FilmResponse


class SessionCreate(BaseModel):
    film_id: int
    start_time: Optional[datetime] = None


class SessionResponse(BaseModel):
    id: int
    film: FilmResponse
    start_time: datetime


class SessionsResponse(BaseModel):
    id: int
    film: List[FilmResponse]
    start_time: datetime
