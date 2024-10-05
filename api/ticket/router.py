from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user import utils as ut

from .schemes import TicketCreate, UpdateTicket, TicketResponse
from . import queries as qr
from . import validators as validator


router = APIRouter(prefix="/tickets")


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_create: TicketCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.admin_check(current_user)
    created_ticket = await qr.create_ticket(session, ticket_create)
    return await validator.ticket_to_pydantic(session, created_ticket)


@router.get("/", response_model=List[TicketResponse])
async def get_tikcets(
    session: AsyncSession = Depends(get_session),
):
    tickets = await qr.get_all_tikcets(session)
    return await validator.list_tickets_to_pydantic(session, tickets)


@router.patch("/tickets/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    ticket_data: UpdateTicket,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.admin_check(current_user)
    updated_ticket = await qr.update_ticket(session, ticket_id, ticket_data)
    return await validator.ticket_to_pydantic(session, updated_ticket)


@router.delete("/tickets/{ticket_id}", status_code=status.HTTP_200_OK)
async def delete_ticket(
    ticket_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.admin_check(current_user)
    await qr.delete_ticket(session, ticket_id)
    return "Билет удалён"
