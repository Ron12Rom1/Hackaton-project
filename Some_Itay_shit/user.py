from enum import Enum
from typing import Dict, List, Optional, Union
from datetime import datetime
import json
import os

class UserType(Enum):
    """Enum representing different types of users in the system"""
    SOLDIER = "soldier"
    EVACUEE = "evacuee"
    PSYCHOLOGIST = "psychologist"

class CombatRole(Enum):
    """Enum representing different combat roles in the IDF"""
    FIGHTER = "fighter"
    DRIVER = "driver"
    MEDIC = "medic"
    COMMANDER = "commander"
    INTELLIGENCE = "intelligence"
    TECHNICAL = "technical"
    LOGISTICS = "logistics"
    OTHER = "other"

class User:
    """Base class for all users in the system"""
    
    def __init__(self, 
                 user_id: str,
                 first_name: str,
                 last_name: str,
                 user_type: UserType,
                 phone: Optional[str] = None,
                 email: Optional[str] = None,
                 profile_image: Optional[str] = None):
        """
        Initialize a new user
        
        Args:
            user_id: Unique identifier for the user
            first_name: User's first name
            last_name: User's last name
            user_type: Type of user (soldier, evacuee, or psychologist)
            phone: Optional phone number
            email: Optional email address
            profile_image: Optional path to profile image
        """
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_type = user_type
        self.phone = phone
        self.email = email
        self.profile_image = profile_image
        self.created_at = datetime.now()
        self.last_login = None
        self.is_active = True
        self.preferences: Dict[str, Union[str, bool, List[str]]] = {}
        self.notifications: List[Dict[str, Union[str, datetime, bool]]] = []
    
    @property
    def full_name(self) -> str:
        """Get the user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def update_profile(self, 
                      first_name: Optional[str] = None,
                      last_name: Optional[str] = None,
                      phone: Optional[str] = None,
                      email: Optional[str] = None,
                      profile_image: Optional[str] = None) -> None:
        """
        Update user profile information
        
        Args:
            first_name: New first name
            last_name: New last name
            phone: New phone number
            email: New email address
            profile_image: New profile image path
        """
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if phone:
            self.phone = phone
        if email:
            self.email = email
        if profile_image:
            self.profile_image = profile_image
    
    def set_preference(self, key: str, value: Union[str, bool, List[str]]) -> None:
        """
        Set a user preference
        
        Args:
            key: Preference key
            value: Preference value
        """
        self.preferences[key] = value
    
    def get_preference(self, key: str, default: any = None) -> any:
        """
        Get a user preference
        
        Args:
            key: Preference key
            default: Default value if preference not found
            
        Returns:
            The preference value or default if not found
        """
        return self.preferences.get(key, default)
    
    def add_notification(self, 
                        message: str,
                        notification_type: str = "info",
                        is_read: bool = False) -> None:
        """
        Add a notification for the user
        
        Args:
            message: Notification message
            notification_type: Type of notification (info, warning, error)
            is_read: Whether the notification has been read
        """
        self.notifications.append({
            "message": message,
            "type": notification_type,
            "timestamp": datetime.now(),
            "is_read": is_read
        })
    
    def mark_notification_read(self, index: int) -> None:
        """
        Mark a notification as read
        
        Args:
            index: Index of the notification to mark as read
        """
        if 0 <= index < len(self.notifications):
            self.notifications[index]["is_read"] = True
    
    def get_unread_notifications(self) -> List[Dict[str, Union[str, datetime, bool]]]:
        """
        Get all unread notifications
        
        Returns:
            List of unread notifications
        """
        return [n for n in self.notifications if not n["is_read"]]
    
    def to_dict(self) -> Dict[str, any]:
        """
        Convert user to dictionary format
        
        Returns:
            Dictionary representation of the user
        """
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_type": self.user_type.value,
            "phone": self.phone,
            "email": self.email,
            "profile_image": self.profile_image,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_active": self.is_active,
            "preferences": self.preferences,
            "notifications": self.notifications
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'User':
        """
        Create a user from dictionary data
        
        Args:
            data: Dictionary containing user data
            
        Returns:
            New User instance
        """
        user = cls(
            user_id=data["user_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            user_type=UserType(data["user_type"]),
            phone=data.get("phone"),
            email=data.get("email"),
            profile_image=data.get("profile_image")
        )
        
        user.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("last_login"):
            user.last_login = datetime.fromisoformat(data["last_login"])
        user.is_active = data["is_active"]
        user.preferences = data["preferences"]
        user.notifications = data["notifications"]
        
        return user
    
    def save_to_file(self, directory: str = "data") -> None:
        """
        Save user data to a JSON file
        
        Args:
            directory: Directory to save the file in
        """
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"user_{self.user_id}.json")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)
    
    @classmethod
    def load_from_file(cls, user_id: str, directory: str = "data") -> Optional['User']:
        """
        Load user data from a JSON file
        
        Args:
            user_id: ID of the user to load
            directory: Directory containing the user file
            
        Returns:
            User instance if found, None otherwise
        """
        file_path = os.path.join(directory, f"user_{user_id}.json")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return None 