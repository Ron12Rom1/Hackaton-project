from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class ChatType(str, Enum):
    PRIVATE = "private"
    GROUP = "group"
    SUPPORT = "support"

class Chat(BaseModel):
    id: str
    name: str
    chat_type: ChatType
    participant_ids: List[str]
    created_at: datetime
    last_message_at: Optional[datetime] = None
    is_active: bool = True

class ChatCreate(BaseModel):
    name: str
    chat_type: ChatType
    participant_ids: List[str]

class ChatUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None 