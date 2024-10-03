import pytz
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from ..film.models import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    film_id = Column(Integer, ForeignKey("films.id"), nullable=False)
    start_time = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Europe/Moscow")),
        nullable=False,
    )

    film = relationship("Film", back_populates="sessions")
    tickets = relationship("Ticket", back_populates="session")
