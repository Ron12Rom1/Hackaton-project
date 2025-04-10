from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLAlchemyEnum
from datetime import datetime
from .base import BaseModel
from Some_Itay_shit.models.user import UserType

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, nullable=True)
    phone = Column(String, nullable=True)
    hashed_password = Column(String)
    user_type = Column(SQLAlchemyEnum(UserType))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True) 