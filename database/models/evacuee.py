from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Evacuee(BaseModel):
    __tablename__ = "evacuees"

    user_id = Column(String, ForeignKey("users.id"), unique=True)
    city = Column(String)
    settlement = Column(String)
    family_members = Column(JSON, default=list)
    special_needs = Column(JSON, default=list)
    medical_conditions = Column(JSON, default=list)
    psychological_support = Column(JSON, default=list)

    user = relationship("User", backref="evacuee_profile") 