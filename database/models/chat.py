from sqlalchemy import Column, String, Boolean, DateTime, JSON, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .base import BaseModel
from ...models.chat import ChatType

class Chat(BaseModel):
    __tablename__ = "chats"

    name = Column(String)
    chat_type = Column(SQLAlchemyEnum(ChatType))
    participant_ids = Column(JSON, default=list)
    last_message_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan") 