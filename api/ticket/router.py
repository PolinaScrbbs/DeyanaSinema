from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.utils import cashier_check

from .schemes import TicketCreate, TicketResponse
from . import queries as qr
from . import validators as validator


router = APIRouter(prefix="/tickets")


@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket_create: TicketCreate,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user)
):
    created_ticket = await qr.create_ticket(session, ticket_create)
    return await validator.ticket_to_pydantic(session, created_ticket)
