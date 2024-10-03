from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
import jwt
import bcrypt

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from enum import Enum as BaseEnum

from config import SECRET_KEY

class Base(DeclarativeBase):
    pass

class Role(BaseEnum):
    USER = "Пользователь"
    CASHIER = "Кассир"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    hashed_password = Column(String(512), nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    # email = Column(String(30), unique=True)
    full_name = Column(String(40), nullable=False)

    tokens = relationship("Token", back_populates="user")

    async def set_password(self, password: str) -> None:
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    async def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.hashed_password.encode("utf-8")
        )

    async def generate_token(self, expires_in: int = 4800) -> str:
        payload = {
            "user_id": self.id,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in),
        }
        print(f"SECRET_KEY: {SECRET_KEY} (type: {type(SECRET_KEY)})")
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String(256), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="token")

    async def verify_token(self, session: AsyncSession, user: Optional[User]):
        try:
            jwt.decode(self.token, SECRET_KEY, algorithms=["HS256"])
            return status.HTTP_200_OK, "The user's token has been verified", self

        except jwt.ExpiredSignatureError:
            return await self.refresh_token(session, user)

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def refresh_token(self, session: AsyncSession, user: Optional[User]):
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_token = await user.generate_token()

        self.token = new_token
        session.add(self)
        await session.commit()

        return status.HTTP_200_OK, "The user's token has been updated", self
    
    user = relationship("User", back_populates="tokens")