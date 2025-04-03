from typing import Dict, List, Optional, Union
from datetime import datetime
from .user import User, UserType

class Evacuee(User):
    """Class representing an evacuee in the system"""
    
    def __init__(self,
                 user_id: str,
                 first_name: str,
                 last_name: str,
                 evacuated_from: str,
                 evacuated_to: str,
                 evacuation_date: Optional[datetime] = None,
                 family_size: Optional[int] = None,
                 special_needs: Optional[List[str]] = None,
                 accommodation_type: Optional[str] = None,
                 phone: Optional[str] = None,
                 email: Optional[str] = None,
                 profile_image: Optional[str] = None):
        """
        Initialize a new evacuee
        
        Args:
            user_id: Unique identifier for the evacuee
            first_name: Evacuee's first name
            last_name: Evacuee's last name
            evacuated_from: Location evacuated from
            evacuated_to: Location evacuated to
            evacuation_date: Optional date of evacuation
            family_size: Optional number of family members
            special_needs: Optional list of special needs
            accommodation_type: Optional type of accommodation
            phone: Optional phone number
            email: Optional email address
            profile_image: Optional path to profile image
        """
        super().__init__(user_id, first_name, last_name, UserType.EVACUEE, phone, email, profile_image)
        self.evacuated_from = evacuated_from
        self.evacuated_to = evacuated_to
        self.evacuation_date = evacuation_date or datetime.now()
        self.family_size = family_size
        self.special_needs = special_needs or []
        self.accommodation_type = accommodation_type
        self.contact_info: Dict[str, str] = {}
        self.emergency_contact: Optional[Dict[str, str]] = None
        self.has_pets: bool = False
        self.pet_details: Optional[Dict[str, Union[str, List[str]]]] = None
        self.medical_conditions: List[Dict[str, Union[str, datetime, str]]] = []
        self.notes: List[Dict[str, Union[str, datetime]]] = []
        self.support_requests: List[Dict[str, Union[str, datetime, bool]]] = []
    
    def set_contact_info(self,
                        phone: Optional[str] = None,
                        email: Optional[str] = None,
                        address: Optional[str] = None) -> None:
        """
        Set contact information
        
        Args:
            phone: Phone number
            email: Email address
            address: Physical address
        """
        if phone:
            self.contact_info["phone"] = phone
        if email:
            self.contact_info["email"] = email
        if address:
            self.contact_info["address"] = address
    
    def set_emergency_contact(self,
                            name: str,
                            relationship: str,
                            phone: str,
                            email: Optional[str] = None) -> None:
        """
        Set emergency contact information
        
        Args:
            name: Contact's name
            relationship: Relationship to evacuee
            phone: Contact's phone number
            email: Optional email address
        """
        self.emergency_contact = {
            "name": name,
            "relationship": relationship,
            "phone": phone,
            "email": email
        }
    
    def set_pet_info(self,
                    has_pets: bool,
                    pet_types: Optional[List[str]] = None,
                    pet_names: Optional[List[str]] = None,
                    special_care: Optional[List[str]] = None) -> None:
        """
        Set pet information
        
        Args:
            has_pets: Whether the evacuee has pets
            pet_types: Optional list of pet types
            pet_names: Optional list of pet names
            special_care: Optional list of special care requirements
        """
        self.has_pets = has_pets
        if has_pets:
            self.pet_details = {
                "types": pet_types or [],
                "names": pet_names or [],
                "special_care": special_care or []
            }
    
    def add_medical_condition(self,
                            condition: str,
                            diagnosed_date: datetime,
                            doctor: str,
                            treatment: Optional[str] = None,
                            notes: Optional[str] = None) -> None:
        """
        Add a medical condition
        
        Args:
            condition: Name of medical condition
            diagnosed_date: When condition was diagnosed
            doctor: Name of doctor
            treatment: Optional treatment prescribed
            notes: Optional additional notes
        """
        record = {
            "condition": condition,
            "diagnosed_date": diagnosed_date,
            "doctor": doctor,
            "treatment": treatment,
            "notes": notes
        }
        self.medical_conditions.append(record)
    
    def add_note(self,
                content: str,
                category: Optional[str] = None) -> None:
        """
        Add a note
        
        Args:
            content: Note content
            category: Optional note category
        """
        note = {
            "content": content,
            "category": category,
            "timestamp": datetime.now()
        }
        self.notes.append(note)
    
    def add_support_request(self,
                          request_type: str,
                          description: str,
                          priority: str = "medium",
                          is_urgent: bool = False) -> None:
        """
        Add a support request
        
        Args:
            request_type: Type of support needed
            description: Detailed description of request
            priority: Request priority (low, medium, high)
            is_urgent: Whether the request is urgent
        """
        request = {
            "type": request_type,
            "description": description,
            "priority": priority,
            "is_urgent": is_urgent,
            "timestamp": datetime.now(),
            "status": "pending"
        }
        self.support_requests.append(request)
    
    def get_active_support_requests(self) -> List[Dict[str, Union[str, datetime, bool]]]:
        """
        Get all active support requests
        
        Returns:
            List of active support requests
        """
        return [r for r in self.support_requests if r["status"] == "pending"]
    
    def get_evacuation_duration(self) -> int:
        """
        Calculate the evacuation duration in days
        
        Returns:
            Number of days since evacuation
        """
        return (datetime.now() - self.evacuation_date).days
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert evacuee to dictionary format
        
        Returns:
            Dictionary representation of the evacuee
        """
        data = super().to_dict()
        data.update({
            "evacuated_from": self.evacuated_from,
            "evacuated_to": self.evacuated_to,
            "evacuation_date": self.evacuation_date.isoformat(),
            "family_size": self.family_size,
            "special_needs": self.special_needs,
            "accommodation_type": self.accommodation_type,
            "contact_info": self.contact_info,
            "emergency_contact": self.emergency_contact,
            "has_pets": self.has_pets,
            "pet_details": self.pet_details,
            "medical_conditions": self.medical_conditions,
            "notes": self.notes,
            "support_requests": self.support_requests
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Evacuee':
        """
        Create an evacuee from dictionary data
        
        Args:
            data: Dictionary containing evacuee data
            
        Returns:
            New Evacuee instance
        """
        evacuee = cls(
            user_id=data["user_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            evacuated_from=data["evacuated_from"],
            evacuated_to=data["evacuated_to"],
            evacuation_date=datetime.fromisoformat(data["evacuation_date"]),
            family_size=data.get("family_size"),
            special_needs=data.get("special_needs"),
            accommodation_type=data.get("accommodation_type"),
            phone=data.get("phone"),
            email=data.get("email"),
            profile_image=data.get("profile_image")
        )
        
        evacuee.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("last_login"):
            evacuee.last_login = datetime.fromisoformat(data["last_login"])
        evacuee.is_active = data["is_active"]
        evacuee.preferences = data["preferences"]
        evacuee.notifications = data["notifications"]
        evacuee.contact_info = data["contact_info"]
        evacuee.emergency_contact = data["emergency_contact"]
        evacuee.has_pets = data["has_pets"]
        evacuee.pet_details = data["pet_details"]
        evacuee.medical_conditions = data["medical_conditions"]
        evacuee.notes = data["notes"]
        evacuee.support_requests = data["support_requests"]
        
        return evacuee 