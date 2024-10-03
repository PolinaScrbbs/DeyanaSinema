from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_session
from ..auth.queries import get_current_user
from ..user.models import User
from ..user.utils import cashier_check

from .schemes import SessionCreate, SessionResponse
from . import queries as qr
from . import validators as validator

router = APIRouter(prefix="/sessions")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_session(
    session_create: SessionCreate,
    async_session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await cashier_check(current_user)
    created_session = await qr.create_session(async_session, session_create)
    return await validator.session_to_pydantic(async_session, created_session)


@router.get("/", response_model=List[SessionResponse])
async def get_all_sessions(async_session: AsyncSession = Depends(get_session)):
    film_sessions = await qr.get_all_sessions(async_session)
    return await validator.list_sessions_to_pydantic(async_session, film_sessions)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session_by_id(
    session_id: int, async_session: AsyncSession = Depends(get_session)
):
    film_session = await qr.get_session_by_id(async_session, session_id)
    return await validator.session_to_pydantic(async_session, film_session)
