from fastapi import APIRouter
from app.schemas.symptom_schema import SymptomRequest, SymptomResponse
from app.services.symptom_service import analyze_symptoms

router = APIRouter()

@router.post("/check-symptoms", response_model=SymptomResponse)
async def check_symptoms(request: SymptomRequest):
    return analyze_symptoms(request.symptoms) #(to be changed later)
