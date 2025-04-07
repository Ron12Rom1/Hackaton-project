from enum import Enum
from typing import Optional
from pydantic import BaseModel
from .user import UserBase, UserCreate, User

class CombatRole(str, Enum):
    COMMANDER = "commander"
    MEDIC = "medic"
    ENGINEER = "engineer"
    INFANTRY = "infantry"

class SoldierBase(UserBase):
    unit: str
    combat_role: CombatRole

class SoldierCreate(SoldierBase, UserCreate):
    pass

class Soldier(SoldierBase, User):
    pass 