from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime

from .models import Role


class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str
    full_name: str


class BaseUser(BaseModel):
    id: int
    username: str
    role: str
    full_name: str


class UserResponse(BaseModel):
    message: str
    user: BaseUser
