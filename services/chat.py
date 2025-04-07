from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from .base import BaseService
from ..database.models import Chat, Message, User
from ..models.chat import ChatType

class ChatService(BaseService[Chat]):
    def __init__(self, db: Session):
        super().__init__(Chat, db)

    def create_chat(self, data: Dict[str, Any]) -> Chat:
        chat = super().create(data)
        return chat

    def get_user_chats(self, user_id: str) -> List[Chat]:
        return (
            self.db.query(Chat)
            .filter(Chat.participant_ids.contains([user_id]))
            .filter(Chat.is_active == True)
            .all()
        )

    def add_participant(self, chat_id: str, user_id: str) -> Optional[Chat]:
        chat = self.get(chat_id)
        if chat and user_id not in chat.participant_ids:
            chat.participant_ids.append(user_id)
            self.db.commit()
            self.db.refresh(chat)
        return chat

    def remove_participant(self, chat_id: str, user_id: str) -> Optional[Chat]:
        chat = self.get(chat_id)
        if chat and user_id in chat.participant_ids:
            chat.participant_ids.remove(user_id)
            self.db.commit()
            self.db.refresh(chat)
        return chat

    def send_message(self, chat_id: str, sender_id: str, content: str, is_ai: bool = False) -> Optional[Message]:
        chat = self.get(chat_id)
        if not chat or sender_id not in chat.participant_ids:
            return None

        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            content=content,
            is_ai=is_ai
        )
        self.db.add(message)
        
        chat.last_message_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages(self, chat_id: str, limit: int = 50) -> List[Message]:
        return (
            self.db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .all()
        )

    def mark_message_as_read(self, message_id: str, user_id: str) -> Optional[Message]:
        message = self.db.query(Message).filter(Message.id == message_id).first()
        if message and message.sender_id != user_id:
            message.is_read = True
            self.db.commit()
            self.db.refresh(message)
        return message

    def get_unread_messages(self, user_id: str) -> List[Message]:
        user_chats = self.get_user_chats(user_id)
        chat_ids = [chat.id for chat in user_chats]
        return (
            self.db.query(Message)
            .filter(Message.chat_id.in_(chat_ids))
            .filter(Message.sender_id != user_id)
            .filter(Message.is_read == False)
            .all()
        ) 