from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship

from ..user.models import Base, BaseEnum


class AgeRating(BaseEnum):
    G = "Для всех возрастов"
    PG = "Рекомендуется присутствие родителей"
    PG_13 = "Детям до 13 лет просмотр не желателен"
    R = "Лица до 17 лет допускаются с родителями"
    NC_17 = "Лица до 17 лет не допускаются"
    TV_MA = "Только для взрослых"


film_genre = Table(
    "film_genre",
    Base.metadata,
    Column("film_id", Integer, ForeignKey("films.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True, nullable=False)
    description = Column(String(200), nullable=False)
    age_rating = Column(Enum(AgeRating), default=AgeRating.PG_13, nullable=False)
    duration = Column(Integer, default=120, nullable=False)
    release_year = Column(Integer, default=2024, nullable=False)

    genres = relationship("Genre", secondary="film_genre", back_populates="films")


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True, nullable=False)

    films = relationship("Film", secondary="film_genre", back_populates="genres")
