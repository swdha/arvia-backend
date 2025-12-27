from app.rag.generation_service import generate_answer
from app.agents.query_refiner import refine_query
from app.agents.severity_assessor import assess_severity

def analyze_symptoms(user_input: str):
    """
    Main analysis pipeline with both agents.
    
    Flow: User input → Agent-1 refines → Agent-2 assesses → RAG generates
    """
    
    # Step 1: Refine the query (Agent-1)
    # Converts casual language to medical terms
    refined = refine_query(user_input)
    # passing agent 1 result to agent 2
    # Step 2: Assess severity (Agent-2)
    # Determines if symptoms are mild/moderate/severe
    assessment = assess_severity(refined["refined_query"])
    
    # Step 3: Generate response based on severity   this is where routing happens
    # Different handling for different severity levels
    if assessment["severity"] == "SEVERE":
        # Severe case: urgent message + RAG response
        answer = generate_answer(refined["refined_query"])
        urgent_note = "URGENT: These symptoms require immediate medical attention. Please seek emergency care."
        answer = f"{urgent_note}\n\n{answer}"
        
    elif assessment["severity"] == "MODERATE":
        # Moderate: normal RAG response + doctor recommendation
        answer = generate_answer(refined["refined_query"])    #(need for doc=true, flag in metadata)
        
    else:  # MILD
        # Mild: RAG response with self-care emphasis
        answer = generate_answer(refined["refined_query"])
    
    # Step 4: Build response with all metadata, returning all metadata for transparency among users
    return {
        "answer": answer,
        "original_query": refined["original_query"],
        "refined_query": refined["refined_query"],
        "severity": assessment["severity"],
        "severity_reasoning": assessment["reasoning"],
        "needs_doctor": assessment["needs_doctor"],
        "needs_clarification": refined["needs_clarification"],
        "disclaimer": "This is not a medical diagnosis. Consult a healthcare professional."
    }