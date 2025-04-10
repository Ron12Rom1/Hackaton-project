from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
from .user import UserBase, UserCreate, User

class Specialization(str, Enum):
    TRAUMA = "trauma"
    PTSD = "ptsd"
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    FAMILY = "family"
    CHILD = "child"

class Availability(BaseModel):
    day: str
    start_time: str
    end_time: str

class PsychologistBase(UserBase):
    specialization: Specialization

class PsychologistCreate(PsychologistBase, UserCreate):
    pass

class Psychologist(PsychologistBase, User):
    availability: List[Availability] = []
    max_patients: int = 10
    current_patients: List[str] = [] 