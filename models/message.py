from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"

class Message(BaseModel):
    id: str
    chat_id: str
    sender_id: str
    content: str
    message_type: MessageType = MessageType.TEXT
    timestamp: datetime
    is_read: bool = False
    is_ai: bool = False

class MessageCreate(BaseModel):
    chat_id: str
    content: str
    message_type: MessageType = MessageType.TEXT
    is_ai: bool = False

class MessageUpdate(BaseModel):
    is_read: Optional[bool] = None 