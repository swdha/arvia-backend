from app.rag.generation_service import generate_answer, extract_remedies
from app.agents.query_refiner import refine_query
from app.agents.severity_assessor import assess_severity
from app.agents.doctor_finder import determine_specialization, find_nearby_doctors

def analyze_symptoms(user_input: str, user_location: dict = None):
    """
    Main symptom analysis pipeline.
    Runs Agent-1 → Agent-2 → Agent-3 (if needed) → RAG
    """
    
    # Step 1: Refine the query (Agent-1)
    # Converts casual language to medical terms
    refined = refine_query(user_input)
    # passing agent 1 result to agent 2
    # Step 2: Assess severity (Agent-2)
    # Determines if symptoms are mild/moderate/severe
    assessment = assess_severity(refined["refined_query"])

    # Agent-3: find doctors if needed
    recommended_spec = None
    doctors_list = []
    
    
    if assessment["needs_doctor"]:
        # Determine doctor type
        recommended_spec = determine_specialization(
            symptoms=refined["refined_query"],
            severity=assessment["severity"]
        )
        
        # Find nearby if location provided
        if user_location and "latitude" in user_location and "longitude" in user_location:
            result = find_nearby_doctors(
                specialization=recommended_spec,
                latitude=user_location["latitude"],
                longitude=user_location["longitude"]
            )
            
            if result["success"]:
                doctors_list = result["doctors"]
    
    # NEW: Extract remedies for MILD cases
    remedies_list = []
    
    # Generate RAG answer based on severity
    if assessment["severity"] == "SEVERE":
        answer = generate_answer(refined["refined_query"])
        answer = f" URGENT: Seek immediate medical attention.\n\n{answer}"
        
    elif assessment["severity"] == "MODERATE":
        answer = generate_answer(refined["refined_query"])
        if recommended_spec:
            answer += f"\n\nRecommended: {recommended_spec}"
        
    else:
        # MILD case - extract remedies from vector DB
        answer = generate_answer(refined["refined_query"])
        remedies_list = extract_remedies(refined["refined_query"])
    
    # Return everything
    return {
        "answer": answer,
        "disclaimer": "This is not a diagnosis. Consult a healthcare professional.",
        "original_query": refined["original_query"],
        "refined_query": refined["refined_query"],
        "needs_clarification": refined["needs_clarification"],
        "severity": assessment["severity"],
        "severity_reasoning": assessment["reasoning"],
        "needs_doctor": assessment["needs_doctor"],
        "recommended_specialization": recommended_spec,
        "doctors_nearby": doctors_list,
        "remedies": remedies_list  # NEW: Add remedies to response
    }