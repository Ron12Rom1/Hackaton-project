from typing import Dict, List, Optional, Union
from datetime import datetime
from .user import User, UserType, CombatRole

class Soldier(User):
    """Class representing a soldier in the system"""
    
    def __init__(self,
                 user_id: str,
                 first_name: str,
                 last_name: str,
                 combat_role: CombatRole,
                 unit: str,
                 rank: Optional[str] = None,
                 service_start_date: Optional[datetime] = None,
                 phone: Optional[str] = None,
                 email: Optional[str] = None,
                 profile_image: Optional[str] = None):
        """
        Initialize a new soldier
        
        Args:
            user_id: Unique identifier for the soldier
            first_name: Soldier's first name
            last_name: Soldier's last name
            combat_role: Soldier's combat role
            unit: Soldier's unit
            rank: Optional military rank
            service_start_date: Optional date when service started
            phone: Optional phone number
            email: Optional email address
            profile_image: Optional path to profile image
        """
        super().__init__(user_id, first_name, last_name, UserType.SOLDIER, phone, email, profile_image)
        self.combat_role = combat_role
        self.unit = unit
        self.rank = rank
        self.service_start_date = service_start_date or datetime.now()
        self.deployments: List[Dict[str, Union[str, datetime]]] = []
        self.training_records: List[Dict[str, Union[str, datetime, str]]] = []
        self.medical_records: List[Dict[str, Union[str, datetime, str]]] = []
        self.emergency_contacts: List[Dict[str, str]] = []
    
    def add_deployment(self,
                      location: str,
                      start_date: datetime,
                      end_date: Optional[datetime] = None,
                      description: Optional[str] = None) -> None:
        """
        Add a deployment record
        
        Args:
            location: Deployment location
            start_date: When deployment started
            end_date: Optional end date of deployment
            description: Optional description of deployment
        """
        deployment = {
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description
        }
        self.deployments.append(deployment)
    
    def add_training_record(self,
                          training_type: str,
                          completion_date: datetime,
                          instructor: str,
                          grade: Optional[str] = None,
                          notes: Optional[str] = None) -> None:
        """
        Add a training record
        
        Args:
            training_type: Type of training completed
            completion_date: When training was completed
            instructor: Name of instructor
            grade: Optional grade received
            notes: Optional notes about the training
        """
        record = {
            "type": training_type,
            "completion_date": completion_date,
            "instructor": instructor,
            "grade": grade,
            "notes": notes
        }
        self.training_records.append(record)
    
    def add_medical_record(self,
                          record_type: str,
                          date: datetime,
                          doctor: str,
                          diagnosis: str,
                          treatment: Optional[str] = None,
                          notes: Optional[str] = None) -> None:
        """
        Add a medical record
        
        Args:
            record_type: Type of medical record
            date: Date of medical event
            doctor: Name of doctor
            diagnosis: Medical diagnosis
            treatment: Optional treatment prescribed
            notes: Optional additional notes
        """
        record = {
            "type": record_type,
            "date": date,
            "doctor": doctor,
            "diagnosis": diagnosis,
            "treatment": treatment,
            "notes": notes
        }
        self.medical_records.append(record)
    
    def add_emergency_contact(self,
                            name: str,
                            relationship: str,
                            phone: str,
                            email: Optional[str] = None,
                            address: Optional[str] = None) -> None:
        """
        Add an emergency contact
        
        Args:
            name: Contact's name
            relationship: Relationship to soldier
            phone: Contact's phone number
            email: Optional email address
            address: Optional physical address
        """
        contact = {
            "name": name,
            "relationship": relationship,
            "phone": phone,
            "email": email,
            "address": address
        }
        self.emergency_contacts.append(contact)
    
    def get_active_deployment(self) -> Optional[Dict[str, Union[str, datetime]]]:
        """
        Get the soldier's current deployment if any
        
        Returns:
            Current deployment record if active, None otherwise
        """
        now = datetime.now()
        for deployment in self.deployments:
            if deployment["end_date"] is None or deployment["end_date"] > now:
                return deployment
        return None
    
    def get_service_duration(self) -> int:
        """
        Calculate the soldier's service duration in days
        
        Returns:
            Number of days in service
        """
        return (datetime.now() - self.service_start_date).days
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert soldier to dictionary format
        
        Returns:
            Dictionary representation of the soldier
        """
        data = super().to_dict()
        data.update({
            "combat_role": self.combat_role.value,
            "unit": self.unit,
            "rank": self.rank,
            "service_start_date": self.service_start_date.isoformat(),
            "deployments": self.deployments,
            "training_records": self.training_records,
            "medical_records": self.medical_records,
            "emergency_contacts": self.emergency_contacts
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Soldier':
        """
        Create a soldier from dictionary data
        
        Args:
            data: Dictionary containing soldier data
            
        Returns:
            New Soldier instance
        """
        soldier = cls(
            user_id=data["user_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            combat_role=CombatRole(data["combat_role"]),
            unit=data["unit"],
            rank=data.get("rank"),
            service_start_date=datetime.fromisoformat(data["service_start_date"]),
            phone=data.get("phone"),
            email=data.get("email"),
            profile_image=data.get("profile_image")
        )
        
        soldier.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("last_login"):
            soldier.last_login = datetime.fromisoformat(data["last_login"])
        soldier.is_active = data["is_active"]
        soldier.preferences = data["preferences"]
        soldier.notifications = data["notifications"]
        soldier.deployments = data["deployments"]
        soldier.training_records = data["training_records"]
        soldier.medical_records = data["medical_records"]
        soldier.emergency_contacts = data["emergency_contacts"]
        
        return soldier 