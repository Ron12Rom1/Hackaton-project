from typing import Optional, List
from pydantic import BaseModel
from .user import UserBase, UserCreate, User

class FamilyMember(BaseModel):
    first_name: str
    last_name: str
    relationship: str
    age: int
    special_needs: Optional[List[str]] = None

class MedicalCondition(BaseModel):
    condition: str
    diagnosis_date: str
    treatment: Optional[str] = None
    notes: Optional[str] = None

class PsychologicalSupport(BaseModel):
    psychologist_id: str
    session_date: str
    notes: Optional[str] = None
    follow_up_date: Optional[str] = None

class EvacueeBase(UserBase):
    city: str
    settlement: str

class EvacueeCreate(EvacueeBase, UserCreate):
    pass

class Evacuee(EvacueeBase, User):
    family_members: List[FamilyMember] = []
    special_needs: List[str] = []
    medical_conditions: List[MedicalCondition] = []
    psychological_support: List[PsychologicalSupport] = [] 