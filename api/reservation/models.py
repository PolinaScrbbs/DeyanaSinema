from datetime import datetime
import pytz

from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..ticket.models import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(ForeignKey("tickets.id"), unique=True, nullable=False)
    booked_user_id = Column(ForeignKey("users.id"), nullable=False)
    cashier_id = Column(ForeignKey("users.id"), nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(pytz.timezone("Europe/Moscow")).replace(
            tzinfo=None
        ),
        nullable=False,
    )

    ticket = relationship("Ticket", back_populates="reservation")
    booked_user = relationship(
        "User", foreign_keys=[booked_user_id], back_populates="booked_reservations"
    )
    cashier = relationship(
        "User", foreign_keys=[cashier_id], back_populates="processed_reservations"
    )

    @property
    async def price(self):
        basic_price = self.ticket.basic_price
        room_type = await self.ticket.room_number.type
        extra_charge = await room_type.extra_charge
        return basic_price + basic_price / 100 * extra_charge
