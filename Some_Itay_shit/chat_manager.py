from typing import List, Dict, Optional, Union, Set
from datetime import datetime
import json
import os
import uuid
from user import User, UserType
from soldier import Soldier
from evacuee import Evacuee
from psychologist import Psychologist

class ChatRoom:
    """Class representing a chat room in the system"""
    
    def __init__(self,
                 room_id: str,
                 name: str,
                 room_type: str,
                 created_by: User,
                 description: Optional[str] = None,
                 is_private: bool = False):
        """
        Initialize a new chat room
        
        Args:
            room_id: Unique identifier for the room
            name: Room name
            room_type: Type of room (soldier, evacuee, psychologist)
            created_by: User who created the room
            description: Optional room description
            is_private: Whether the room is private
        """
        self.room_id = room_id
        self.name = name
        self.room_type = room_type
        self.created_by = created_by
        self.description = description
        self.is_private = is_private
        self.created_at = datetime.now()
        self.messages: List[Dict[str, Union[str, datetime, Dict]]] = []
        self.participants: Set[str] = {created_by.user_id}
        self.moderators: Set[str] = {created_by.user_id}
        self.pinned_messages: List[str] = []  # List of message IDs
        self.settings: Dict[str, Union[bool, str, List[str]]] = {
            "allow_media": True,
            "allow_links": True,
            "slow_mode": False,
            "slow_mode_interval": 5,  # seconds
            "muted_words": []
        }
    
    def add_message(self,
                   sender: User,
                   content: str,
                   message_type: str = "text",
                   media_url: Optional[str] = None,
                   reply_to: Optional[str] = None) -> str:
        """
        Add a new message to the room
        
        Args:
            sender: User sending the message
            content: Message content
            message_type: Type of message (text, image, file, etc.)
            media_url: Optional URL to media content
            reply_to: Optional ID of message being replied to
            
        Returns:
            ID of the new message
        """
        message_id = str(uuid.uuid4())
        message = {
            "message_id": message_id,
            "sender_id": sender.user_id,
            "sender_name": sender.full_name,
            "content": content,
            "type": message_type,
            "media_url": media_url,
            "reply_to": reply_to,
            "timestamp": datetime.now(),
            "edited": False,
            "reactions": {}
        }
        self.messages.append(message)
        return message_id
    
    def edit_message(self,
                    message_id: str,
                    new_content: str,
                    editor: User) -> bool:
        """
        Edit an existing message
        
        Args:
            message_id: ID of message to edit
            new_content: New message content
            editor: User making the edit
            
        Returns:
            True if edit was successful, False otherwise
        """
        for message in self.messages:
            if message["message_id"] == message_id:
                if message["sender_id"] == editor.user_id or editor.user_id in self.moderators:
                    message["content"] = new_content
                    message["edited"] = True
                    message["edited_by"] = editor.user_id
                    message["edited_at"] = datetime.now()
                    return True
                break
        return False
    
    def delete_message(self,
                      message_id: str,
                      deleter: User) -> bool:
        """
        Delete a message
        
        Args:
            message_id: ID of message to delete
            deleter: User deleting the message
            
        Returns:
            True if deletion was successful, False otherwise
        """
        for i, message in enumerate(self.messages):
            if message["message_id"] == message_id:
                if message["sender_id"] == deleter.user_id or deleter.user_id in self.moderators:
                    self.messages.pop(i)
                    return True
                break
        return False
    
    def add_reaction(self,
                    message_id: str,
                    user: User,
                    reaction: str) -> bool:
        """
        Add a reaction to a message
        
        Args:
            message_id: ID of message to react to
            user: User adding the reaction
            reaction: Reaction emoji/text
            
        Returns:
            True if reaction was added, False otherwise
        """
        for message in self.messages:
            if message["message_id"] == message_id:
                if user.user_id not in message["reactions"]:
                    message["reactions"][user.user_id] = []
                if reaction not in message["reactions"][user.user_id]:
                    message["reactions"][user.user_id].append(reaction)
                return True
        return False
    
    def remove_reaction(self,
                       message_id: str,
                       user: User,
                       reaction: str) -> bool:
        """
        Remove a reaction from a message
        
        Args:
            message_id: ID of message to remove reaction from
            user: User removing the reaction
            reaction: Reaction to remove
            
        Returns:
            True if reaction was removed, False otherwise
        """
        for message in self.messages:
            if message["message_id"] == message_id:
                if user.user_id in message["reactions"] and reaction in message["reactions"][user.user_id]:
                    message["reactions"][user.user_id].remove(reaction)
                    if not message["reactions"][user.user_id]:
                        del message["reactions"][user.user_id]
                    return True
        return False
    
    def pin_message(self, message_id: str) -> bool:
        """
        Pin a message to the top of the room
        
        Args:
            message_id: ID of message to pin
            
        Returns:
            True if message was pinned, False otherwise
        """
        for message in self.messages:
            if message["message_id"] == message_id:
                if message_id not in self.pinned_messages:
                    self.pinned_messages.append(message_id)
                return True
        return False
    
    def unpin_message(self, message_id: str) -> bool:
        """
        Unpin a message
        
        Args:
            message_id: ID of message to unpin
            
        Returns:
            True if message was unpinned, False otherwise
        """
        if message_id in self.pinned_messages:
            self.pinned_messages.remove(message_id)
            return True
        return False
    
    def add_participant(self, user: User) -> bool:
        """
        Add a participant to the room
        
        Args:
            user: User to add
            
        Returns:
            True if user was added, False if already present
        """
        if user.user_id not in self.participants:
            self.participants.add(user.user_id)
            return True
        return False
    
    def remove_participant(self, user: User) -> bool:
        """
        Remove a participant from the room
        
        Args:
            user: User to remove
            
        Returns:
            True if user was removed, False if not present
        """
        if user.user_id in self.participants and user.user_id != self.created_by.user_id:
            self.participants.remove(user.user_id)
            if user.user_id in self.moderators:
                self.moderators.remove(user.user_id)
            return True
        return False
    
    def add_moderator(self, user: User) -> bool:
        """
        Add a moderator to the room
        
        Args:
            user: User to make moderator
            
        Returns:
            True if user was made moderator, False if already moderator
        """
        if user.user_id in self.participants and user.user_id not in self.moderators:
            self.moderators.add(user.user_id)
            return True
        return False
    
    def remove_moderator(self, user: User) -> bool:
        """
        Remove a moderator from the room
        
        Args:
            user: User to remove moderator status from
            
        Returns:
            True if moderator status was removed, False otherwise
        """
        if user.user_id in self.moderators and user.user_id != self.created_by.user_id:
            self.moderators.remove(user.user_id)
            return True
        return False
    
    def update_settings(self, settings: Dict[str, Union[bool, str, List[str]]]) -> None:
        """
        Update room settings
        
        Args:
            settings: Dictionary of settings to update
        """
        self.settings.update(settings)
    
    def to_dict(self) -> Dict[str, Union[str, datetime, Dict]]:
        """
        Convert chat room to dictionary format
        
        Returns:
            Dictionary representation of the chat room
        """
        return {
            "room_id": self.room_id,
            "name": self.name,
            "room_type": self.room_type,
            "created_by": self.created_by.user_id,
            "description": self.description,
            "is_private": self.is_private,
            "created_at": self.created_at.isoformat(),
            "messages": self.messages,
            "participants": list(self.participants),
            "moderators": list(self.moderators),
            "pinned_messages": self.pinned_messages,
            "settings": self.settings
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, datetime, Dict]], created_by: User) -> 'ChatRoom':
        """
        Create a chat room from dictionary data
        
        Args:
            data: Dictionary containing chat room data
            created_by: User who created the room
            
        Returns:
            New ChatRoom instance
        """
        room = cls(
            room_id=data["room_id"],
            name=data["name"],
            room_type=data["room_type"],
            created_by=created_by,
            description=data.get("description"),
            is_private=data["is_private"]
        )
        
        room.created_at = datetime.fromisoformat(data["created_at"])
        room.messages = data["messages"]
        room.participants = set(data["participants"])
        room.moderators = set(data["moderators"])
        room.pinned_messages = data["pinned_messages"]
        room.settings = data["settings"]
        
        return room

class ChatManager:
    """Class managing chat rooms and user interactions"""
    
    def __init__(self):
        """Initialize the chat manager"""
        self.rooms: Dict[str, ChatRoom] = {}
        self.user_rooms: Dict[str, Set[str]] = {}  # user_id -> set of room_ids
        self.direct_messages: Dict[str, Dict[str, List[Dict[str, Union[str, datetime, Dict]]]]] = {}  # user_id -> {other_user_id -> messages}
        self.load_data()
    
    def create_room(self,
                   name: str,
                   room_type: str,
                   created_by: User,
                   description: Optional[str] = None,
                   is_private: bool = False) -> ChatRoom:
        """
        Create a new chat room
        
        Args:
            name: Room name
            room_type: Type of room
            created_by: User creating the room
            description: Optional room description
            is_private: Whether the room is private
            
        Returns:
            New ChatRoom instance
        """
        room_id = str(uuid.uuid4())
        room = ChatRoom(room_id, name, room_type, created_by, description, is_private)
        self.rooms[room_id] = room
        
        if created_by.user_id not in self.user_rooms:
            self.user_rooms[created_by.user_id] = set()
        self.user_rooms[created_by.user_id].add(room_id)
        
        self.save_data()
        return room
    
    def get_room(self, room_id: str) -> Optional[ChatRoom]:
        """
        Get a chat room by ID
        
        Args:
            room_id: ID of room to get
            
        Returns:
            ChatRoom instance if found, None otherwise
        """
        return self.rooms.get(room_id)
    
    def get_user_rooms(self, user: User) -> List[ChatRoom]:
        """
        Get all rooms a user is in
        
        Args:
            user: User to get rooms for
            
        Returns:
            List of ChatRoom instances
        """
        room_ids = self.user_rooms.get(user.user_id, set())
        return [self.rooms[room_id] for room_id in room_ids if room_id in self.rooms]
    
    def join_room(self, room: ChatRoom, user: User) -> bool:
        """
        Add a user to a room
        
        Args:
            room: Room to join
            user: User joining the room
            
        Returns:
            True if user was added, False otherwise
        """
        if room.add_participant(user):
            if user.user_id not in self.user_rooms:
                self.user_rooms[user.user_id] = set()
            self.user_rooms[user.user_id].add(room.room_id)
            self.save_data()
            return True
        return False
    
    def leave_room(self, room: ChatRoom, user: User) -> bool:
        """
        Remove a user from a room
        
        Args:
            room: Room to leave
            user: User leaving the room
            
        Returns:
            True if user was removed, False otherwise
        """
        if room.remove_participant(user):
            self.user_rooms[user.user_id].remove(room.room_id)
            if not self.user_rooms[user.user_id]:
                del self.user_rooms[user.user_id]
            self.save_data()
            return True
        return False
    
    def send_direct_message(self,
                          sender: User,
                          recipient: User,
                          content: str,
                          message_type: str = "text",
                          media_url: Optional[str] = None) -> str:
        """
        Send a direct message between users
        
        Args:
            sender: User sending the message
            recipient: User receiving the message
            content: Message content
            message_type: Type of message
            media_url: Optional URL to media content
            
        Returns:
            ID of the new message
        """
        message_id = str(uuid.uuid4())
        message = {
            "message_id": message_id,
            "sender_id": sender.user_id,
            "sender_name": sender.full_name,
            "content": content,
            "type": message_type,
            "media_url": media_url,
            "timestamp": datetime.now(),
            "read": False
        }
        
        # Initialize direct message storage if needed
        if sender.user_id not in self.direct_messages:
            self.direct_messages[sender.user_id] = {}
        if recipient.user_id not in self.direct_messages[sender.user_id]:
            self.direct_messages[sender.user_id][recipient.user_id] = []
        
        if recipient.user_id not in self.direct_messages:
            self.direct_messages[recipient.user_id] = {}
        if sender.user_id not in self.direct_messages[recipient.user_id]:
            self.direct_messages[recipient.user_id][sender.user_id] = []
        
        # Add message to both users' conversation
        self.direct_messages[sender.user_id][recipient.user_id].append(message)
        self.direct_messages[recipient.user_id][sender.user_id].append(message)
        
        self.save_data()
        return message_id
    
    def get_direct_messages(self,
                          user1: User,
                          user2: User,
                          limit: Optional[int] = None) -> List[Dict[str, Union[str, datetime, Dict]]]:
        """
        Get direct messages between two users
        
        Args:
            user1: First user
            user2: Second user
            limit: Optional limit on number of messages to return
            
        Returns:
            List of messages
        """
        if user1.user_id in self.direct_messages and user2.user_id in self.direct_messages[user1.user_id]:
            messages = self.direct_messages[user1.user_id][user2.user_id]
            if limit:
                return messages[-limit:]
            return messages
        return []
    
    def mark_messages_read(self, user: User, other_user: User) -> None:
        """
        Mark all messages from another user as read
        
        Args:
            user: User marking messages as read
            other_user: User whose messages to mark as read
        """
        if user.user_id in self.direct_messages and other_user.user_id in self.direct_messages[user.user_id]:
            for message in self.direct_messages[user.user_id][other_user.user_id]:
                if message["sender_id"] == other_user.user_id:
                    message["read"] = True
            self.save_data()
    
    def get_unread_count(self, user: User) -> int:
        """
        Get total number of unread messages for a user
        
        Args:
            user: User to get unread count for
            
        Returns:
            Number of unread messages
        """
        count = 0
        if user.user_id in self.direct_messages:
            for other_user_id, messages in self.direct_messages[user.user_id].items():
                for message in messages:
                    if message["sender_id"] != user.user_id and not message["read"]:
                        count += 1
        return count
    
    def save_data(self) -> None:
        """Save chat data to files"""
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        
        # Save rooms
        rooms_data = {room_id: room.to_dict() for room_id, room in self.rooms.items()}
        with open(os.path.join(data_dir, "rooms.json"), 'w', encoding='utf-8') as f:
            json.dump(rooms_data, f, ensure_ascii=False, indent=4)
        
        # Save user rooms
        user_rooms_data = {user_id: list(room_ids) for user_id, room_ids in self.user_rooms.items()}
        with open(os.path.join(data_dir, "user_rooms.json"), 'w', encoding='utf-8') as f:
            json.dump(user_rooms_data, f, ensure_ascii=False, indent=4)
        
        # Save direct messages
        with open(os.path.join(data_dir, "direct_messages.json"), 'w', encoding='utf-8') as f:
            json.dump(self.direct_messages, f, ensure_ascii=False, indent=4)
    
    def load_data(self) -> None:
        """Load chat data from files"""
        data_dir = "data"
        
        # Load rooms
        try:
            with open(os.path.join(data_dir, "rooms.json"), 'r', encoding='utf-8') as f:
                rooms_data = json.load(f)
                # Note: Rooms need to be recreated with proper User objects
                # This is handled when users log in and join rooms
        except FileNotFoundError:
            rooms_data = {}
        
        # Load user rooms
        try:
            with open(os.path.join(data_dir, "user_rooms.json"), 'r', encoding='utf-8') as f:
                user_rooms_data = json.load(f)
                self.user_rooms = {user_id: set(room_ids) for user_id, room_ids in user_rooms_data.items()}
        except FileNotFoundError:
            self.user_rooms = {}
        
        # Load direct messages
        try:
            with open(os.path.join(data_dir, "direct_messages.json"), 'r', encoding='utf-8') as f:
                self.direct_messages = json.load(f)
        except FileNotFoundError:
            self.direct_messages = {} 