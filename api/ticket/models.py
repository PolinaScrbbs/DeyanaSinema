from sqlalchemy import Column, Integer, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship

from ..session.models import Base
from ..film.models import BaseEnum


class RoomType(BaseEnum):
    STANDARD = {"title": "Стандартный", "extra_charge": 5}
    COMFORT = {"title": "Комфорт", "extra_charge": 20}
    VIP = {"title": "ВИП", "extra_charge": 52}

    @property
    async def title(self) -> str:
        return self.value["title"]

    @property
    async def extra_charge(self) -> int:
        return self.value["extra_charge"]


class RoomNumber(BaseEnum):
    ROOM_1 = {"number": 1, "type": RoomType.STANDARD}
    ROOM_2 = {"number": 2, "type": RoomType.STANDARD}
    ROOM_3 = {"number": 3, "type": RoomType.STANDARD}
    ROOM_4 = {"number": 4, "type": RoomType.VIP}
    ROOM_5 = {"number": 5, "type": RoomType.VIP}
    ROOM_6 = {"number": 6, "type": RoomType.VIP}
    ROOM_7 = {"number": 7, "type": RoomType.COMFORT}
    ROOM_8 = {"number": 8, "type": RoomType.COMFORT}
    ROOM_9 = {"number": 9, "type": RoomType.COMFORT}

    @property
    async def number(self) -> int:
        return self.value["number"]

    @property
    async def type(self) -> RoomType:
        return self.value["type"]

    @classmethod
    def from_str(cls, room_str: str):
        try:
            return cls[room_str]
        except KeyError:
            raise ValueError(f"Unknown room number: {room_str}")


class TicketRow(BaseEnum):
    ROW_1 = 1
    ROW_2 = 2
    ROW_3 = 3
    ROW_4 = 4
    ROW_5 = 6
    ROW_6 = 6
    ROW_7 = 7


class Place(BaseEnum):
    PLACE_1 = 1
    PLACE_2 = 2
    PLACE_3 = 3
    PLACE_4 = 4
    PLACE_5 = 5
    PLACE_6 = 6
    PLACE_7 = 7
    PLACE_8 = 8
    PLACE_9 = 9
    PLACE_10 = 10


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    basic_price = Column(Numeric, nullable=False)
    room_number = Column(Enum(RoomNumber), default=RoomNumber.ROOM_1, nullable=False)
    row_number = Column(Enum(TicketRow), default=TicketRow.ROW_1, nullable=False)
    place = Column(Enum(Place), default=Place.PLACE_1, nullable=False)

    session = relationship("Session", back_populates="tickets")
    reservation = relationship("Reservation", back_populates="ticket", uselist=False)
