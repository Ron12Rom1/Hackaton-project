from sqlalchemy import Column, String, Boolean, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .base import BaseModel
from ...models.message import MessageType

class Message(BaseModel):
    __tablename__ = "messages"

    chat_id = Column(String, ForeignKey("chats.id"))
    sender_id = Column(String, ForeignKey("users.id"))
    content = Column(String)
    message_type = Column(SQLAlchemyEnum(MessageType), default=MessageType.TEXT)
    is_read = Column(Boolean, default=False)
    is_ai = Column(Boolean, default=False)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User") 