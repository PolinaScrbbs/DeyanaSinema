from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user import utils as ut
from ..ticket.validators import list_tickets_to_pydantic

from .schemes import (
    SessionCreate,
    SessionResponse,
    SessionUpdate,
    SessionResponseWithTickets,
)
from . import queries as qr
from . import validators as validator

router = APIRouter(prefix="/sessions")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_session(
    session_create: SessionCreate,
    async_session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.admin_check(current_user)
    created_session = await qr.create_session(async_session, session_create)
    return await validator.session_to_pydantic(async_session, created_session)


@router.get("/", response_model=List[SessionResponse])
async def get_all_sessions(async_session: AsyncSession = Depends(get_session)):
    film_sessions = await qr.get_all_sessions(async_session)
    return await validator.list_sessions_to_pydantic(async_session, film_sessions)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session_by_id(
    session_id: int,
    async_session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user),
):
    film_session = await qr.get_session_by_id(async_session, session_id)
    return await validator.session_to_pydantic(async_session, film_session)


@router.get("/{session_id}/tickets")
async def get_sesssion_tickets(
    session_id: int,
    async_session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(get_current_user),
):
    session = await qr.get_session_by_id(async_session, session_id)
    pydantic_session = await validator.session_to_pydantic(async_session, session)
    session_tickets = await qr.get_session_tickets(async_session, session_id)
    pydatnic_session_tickets = await list_tickets_to_pydantic(
        async_session, session_tickets
    )

    return SessionResponseWithTickets(
        id=pydantic_session.id,
        film=pydantic_session.film,
        start_time=pydantic_session.start_time,
        tickets=[ticket.dict() for ticket in pydatnic_session_tickets],
    )


@router.patch("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: int,
    session_update: SessionUpdate,
    async_session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.admin_check(current_user)
    updated_session = await qr.update_session(async_session, session_id, session_update)
    return await validator.session_to_pydantic(async_session, updated_session)


@router.delete("/{session_id}", status_code=status.HTTP_200_OK)
async def delete_session(
    session_id: int,
    async_session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await ut.admin_check(current_user)
    await qr.delete_session(async_session, session_id)
    return "Сеанс удалён"
