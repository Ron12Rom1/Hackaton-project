from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserType(str, Enum):
    SOLDIER = "soldier"
    EVACUEE = "evacuee"
    PSYCHOLOGIST = "psychologist"

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    user_type: UserType
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    created_at: datetime
    is_active: bool = True
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str 