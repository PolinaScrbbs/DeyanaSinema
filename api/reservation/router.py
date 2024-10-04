from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user.utils import cashier_check

from .schemes import ReservationCreate, ReservationResponse
from . import queries as qr
from . import validators as validator

router = APIRouter(prefix="/reservations")


@router.post("/", response_model=ReservationResponse)
async def create_reservation(
    reservation_data: ReservationCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await cashier_check(current_user)
    created_reservation = await qr.create_reservation(
        session, reservation_data, current_user.id
    )
    return await validator.reservation_to_pydantic(session, created_reservation)
