from sqlalchemy import Column, String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .base import BaseModel
from ...models.soldier import CombatRole

class Soldier(BaseModel):
    __tablename__ = "soldiers"

    user_id = Column(String, ForeignKey("users.id"), unique=True)
    unit = Column(String)
    combat_role = Column(SQLAlchemyEnum(CombatRole))

    user = relationship("User", backref="soldier_profile") 