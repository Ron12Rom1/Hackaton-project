from typing import Dict, List, Optional, Union
from datetime import datetime
from .user import User, UserType

class Psychologist(User):
    """Class representing a psychologist in the system"""
    
    def __init__(self,
                 user_id: str,
                 first_name: str,
                 last_name: str,
                 license_number: str,
                 specializations: Optional[List[str]] = None,
                 availability: Optional[Dict[str, List[str]]] = None,
                 phone: Optional[str] = None,
                 email: Optional[str] = None,
                 profile_image: Optional[str] = None):
        """
        Initialize a new psychologist
        
        Args:
            user_id: Unique identifier for the psychologist
            first_name: Psychologist's first name
            last_name: Psychologist's last name
            license_number: Professional license number
            specializations: Optional list of specializations
            availability: Optional availability schedule
            phone: Optional phone number
            email: Optional email address
            profile_image: Optional path to profile image
        """
        super().__init__(user_id, first_name, last_name, UserType.PSYCHOLOGIST, phone, email, profile_image)
        self.license_number = license_number
        self.specializations = specializations or []
        self.availability = availability or {}
        self.current_patients: List[Dict[str, Union[str, datetime, Dict]]] = []
        self.patient_history: List[Dict[str, Union[str, datetime, Dict]]] = []
        self.session_notes: List[Dict[str, Union[str, datetime, str]]] = []
        self.emergency_contacts: List[Dict[str, str]] = []
        self.certifications: List[Dict[str, Union[str, datetime]]] = []
    
    def add_specialization(self, specialization: str) -> None:
        """
        Add a specialization
        
        Args:
            specialization: Name of specialization
        """
        if specialization not in self.specializations:
            self.specializations.append(specialization)
    
    def remove_specialization(self, specialization: str) -> None:
        """
        Remove a specialization
        
        Args:
            specialization: Name of specialization to remove
        """
        if specialization in self.specializations:
            self.specializations.remove(specialization)
    
    def set_availability(self,
                        day: str,
                        time_slots: List[str]) -> None:
        """
        Set availability for a specific day
        
        Args:
            day: Day of the week
            time_slots: List of available time slots
        """
        self.availability[day] = time_slots
    
    def add_patient(self,
                   patient_id: str,
                   patient_name: str,
                   start_date: datetime,
                   initial_assessment: Optional[str] = None) -> None:
        """
        Add a new patient
        
        Args:
            patient_id: Patient's ID
            patient_name: Patient's name
            start_date: When treatment started
            initial_assessment: Optional initial assessment notes
        """
        patient = {
            "patient_id": patient_id,
            "patient_name": patient_name,
            "start_date": start_date,
            "initial_assessment": initial_assessment,
            "sessions": [],
            "status": "active"
        }
        self.current_patients.append(patient)
    
    def end_patient_treatment(self,
                            patient_id: str,
                            end_date: datetime,
                            final_notes: Optional[str] = None) -> None:
        """
        End treatment for a patient
        
        Args:
            patient_id: Patient's ID
            end_date: When treatment ended
            final_notes: Optional final notes
        """
        for i, patient in enumerate(self.current_patients):
            if patient["patient_id"] == patient_id:
                patient["end_date"] = end_date
                patient["final_notes"] = final_notes
                patient["status"] = "completed"
                self.patient_history.append(self.current_patients.pop(i))
                break
    
    def add_session_note(self,
                        patient_id: str,
                        session_date: datetime,
                        notes: str,
                        mood: Optional[str] = None,
                        progress: Optional[str] = None) -> None:
        """
        Add notes from a therapy session
        
        Args:
            patient_id: Patient's ID
            session_date: Date of the session
            notes: Session notes
            mood: Optional patient's mood
            progress: Optional progress notes
        """
        session = {
            "patient_id": patient_id,
            "session_date": session_date,
            "notes": notes,
            "mood": mood,
            "progress": progress
        }
        self.session_notes.append(session)
        
        # Add to patient's session history
        for patient in self.current_patients:
            if patient["patient_id"] == patient_id:
                patient["sessions"].append(session)
                break
    
    def add_emergency_contact(self,
                            name: str,
                            role: str,
                            phone: str,
                            email: Optional[str] = None) -> None:
        """
        Add an emergency contact
        
        Args:
            name: Contact's name
            role: Contact's role
            phone: Contact's phone number
            email: Optional email address
        """
        contact = {
            "name": name,
            "role": role,
            "phone": phone,
            "email": email
        }
        self.emergency_contacts.append(contact)
    
    def add_certification(self,
                         name: str,
                         issuing_organization: str,
                         issue_date: datetime,
                         expiry_date: Optional[datetime] = None) -> None:
        """
        Add a professional certification
        
        Args:
            name: Name of certification
            issuing_organization: Organization that issued the certification
            issue_date: When the certification was issued
            expiry_date: Optional expiration date
        """
        certification = {
            "name": name,
            "issuing_organization": issuing_organization,
            "issue_date": issue_date,
            "expiry_date": expiry_date
        }
        self.certifications.append(certification)
    
    def get_active_patients(self) -> List[Dict[str, Union[str, datetime, Dict]]]:
        """
        Get all active patients
        
        Returns:
            List of active patients
        """
        return [p for p in self.current_patients if p["status"] == "active"]
    
    def get_patient_sessions(self, patient_id: str) -> List[Dict[str, Union[str, datetime, str]]]:
        """
        Get all sessions for a specific patient
        
        Args:
            patient_id: Patient's ID
            
        Returns:
            List of patient's sessions
        """
        return [s for s in self.session_notes if s["patient_id"] == patient_id]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert psychologist to dictionary format
        
        Returns:
            Dictionary representation of the psychologist
        """
        data = super().to_dict()
        data.update({
            "license_number": self.license_number,
            "specializations": self.specializations,
            "availability": self.availability,
            "current_patients": self.current_patients,
            "patient_history": self.patient_history,
            "session_notes": self.session_notes,
            "emergency_contacts": self.emergency_contacts,
            "certifications": self.certifications
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Psychologist':
        """
        Create a psychologist from dictionary data
        
        Args:
            data: Dictionary containing psychologist data
            
        Returns:
            New Psychologist instance
        """
        psychologist = cls(
            user_id=data["user_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            license_number=data["license_number"],
            specializations=data.get("specializations"),
            availability=data.get("availability"),
            phone=data.get("phone"),
            email=data.get("email"),
            profile_image=data.get("profile_image")
        )
        
        psychologist.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("last_login"):
            psychologist.last_login = datetime.fromisoformat(data["last_login"])
        psychologist.is_active = data["is_active"]
        psychologist.preferences = data["preferences"]
        psychologist.notifications = data["notifications"]
        psychologist.current_patients = data["current_patients"]
        psychologist.patient_history = data["patient_history"]
        psychologist.session_notes = data["session_notes"]
        psychologist.emergency_contacts = data["emergency_contacts"]
        psychologist.certifications = data["certifications"]
        
        return psychologist 