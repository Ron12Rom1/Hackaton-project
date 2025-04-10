from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
from .base import BaseService
from ..database.models import User, Soldier, Evacuee, Psychologist
from ..models.user import UserType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseService[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user_data: Dict[str, Any]) -> User:
        hashed_password = pwd_context.hash(user_data.pop("password"))
        user_data["hashed_password"] = hashed_password
        user = super().create(user_data)

        # Create specific user profile based on user type
        if user.user_type == UserType.SOLDIER:
            soldier_data = {"user_id": user.id}
            self.db.add(Soldier(**soldier_data))
        elif user.user_type == UserType.EVACUEE:
            evacuee_data = {"user_id": user.id}
            self.db.add(Evacuee(**evacuee_data))
        elif user.user_type == UserType.PSYCHOLOGIST:
            psychologist_data = {"user_id": user.id}
            self.db.add(Psychologist(**psychologist_data))

        self.db.commit()
        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(username)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    def update_last_login(self, user_id: str) -> None:
        user = self.get(user_id)
        if user:
            user.last_login = datetime.utcnow()
            self.db.commit() 