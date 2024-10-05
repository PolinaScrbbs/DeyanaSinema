from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user import utils as ut

from .schemes import ReservationCreate, ReservationResponse
from . import queries as qr
from . import validators as validator

router = APIRouter(prefix="/reservations")


@router.post(
    "/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED
)
async def create_reservation(
    reservation_data: ReservationCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.cashier_check(current_user)
    created_reservation = await qr.create_reservation(
        session, reservation_data, current_user.id
    )
    return await validator.reservation_to_pydantic(session, created_reservation)


@router.get("/", response_model=List[ReservationResponse])
async def get_reservations(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.cashier_check(current_user)
    reservations = await qr.get_all_reservations(session)
    return [
        await validator.reservation_to_pydantic(session, res) for res in reservations
    ]


@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation_by_id(
    reservation_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    reservation = await qr.get_reservation_by_id(session, reservation_id, current_user)
    return await validator.reservation_to_pydantic(session, reservation)


@router.delete("/{reservation_id}", status_code=status.HTTP_200_OK)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.admin_check(current_user)
    await qr.delete_reservation(session, reservation_id)
    return "Резервация удалена"
