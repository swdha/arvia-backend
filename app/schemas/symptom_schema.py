from pydantic import BaseModel
from typing import Optional, List


class SymptomRequest(BaseModel):
    """
    Request model for symptom checking.
    
    Fields:
    - symptoms: User's symptom description (required)
    - latitude: User's location latitude (optional, for doctor finder)
    - longitude: User's location longitude (optional, for doctor finder)
    """
    symptoms: str
    latitude: Optional[float] = None  # Optional: only needed if user wants nearby doctors
    longitude: Optional[float] = None


class DoctorInfo(BaseModel):
    """
    Model for individual doctor/hospital information.
    
    Contains details about one medical facility.
    """
    name: str
    address: str
    distance: str  # Distance in meters (as string like "500m")
    specialization: str  # What type of doctor this is


class SymptomResponse(BaseModel):
    """
    Complete response model with all agent outputs.
    
    Includes:
    - RAG answer
    - Agent-1 metadata (query refinement)
    - Agent-2 metadata (severity assessment)
    - Agent-3 metadata (doctor recommendations) 
    """
    answer: str
    disclaimer: str
    
    # Agent-1: Query Refiner
    original_query: Optional[str] = None
    refined_query: Optional[str] = None
    needs_clarification: Optional[bool] = False
    
    # Agent-2: Severity Assessor
    severity: Optional[str] = None
    severity_reasoning: Optional[str] = None
    severity_factors: Optional[List[str]] = []  # NEW FIELD ADDED - explains why this severity was chosen
    needs_doctor: Optional[bool] = False
    
    # Agent-3: Doctor Finder
    recommended_specialization: Optional[str] = None  # What type of doctor they need
    doctors_nearby: Optional[List[DoctorInfo]] = []  # List of nearby hospitals
    
    # NEW: Remedies field for MILD cases
    remedies: Optional[List[str]] = []  # Home remedies when doctor not needed