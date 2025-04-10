from sqlalchemy import Column, String, ForeignKey, JSON, Integer, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .base import BaseModel
from ...models.psychologist import Specialization

class Psychologist(BaseModel):
    __tablename__ = "psychologists"

    user_id = Column(String, ForeignKey("users.id"), unique=True)
    specialization = Column(SQLAlchemyEnum(Specialization))
    availability = Column(JSON, default=list)
    max_patients = Column(Integer, default=10)
    current_patients = Column(JSON, default=list)

    user = relationship("User", backref="psychologist_profile") 