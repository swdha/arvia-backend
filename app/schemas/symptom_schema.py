from pydantic import BaseModel
from typing import Optional

class SymptomRequest(BaseModel):
    symptoms: str

class SymptomResponse(BaseModel):
    answer: str
    disclaimer: str
    
    # Agent-1 metadata
    original_query: Optional[str] = None   #optional: may not be present so can be None
    refined_query: Optional[str] = None
    needs_clarification: Optional[bool] = False
    
    # Agent-2 metadata (new fields)
    severity: Optional[str] = None
    severity_reasoning: Optional[str] = None   #for transparency
    needs_doctor: Optional[bool] = False