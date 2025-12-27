from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Separate Gemini instance for severity assessment
# Different job from Agent-1, so separate config
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2  # Low temp for consistent severity decisions
)

# Prompt teaches Gemini how to assess severity
prompt = ChatPromptTemplate.from_template("""
You are a medical severity assessor. Analyze symptoms and determine urgency level.

Symptoms: {symptoms}

Classify as:
- MILD: Minor symptoms, self-care sufficient
- MODERATE: Should see doctor soon, not emergency
- SEVERE: Urgent medical attention needed

Red flags for SEVERE:
- Chest pain, difficulty breathing
- Severe pain (8-10/10)
- High fever with confusion
- Loss of consciousness
- Sudden severe symptoms

Consider:
- Symptom combination
- Duration
- Severity indicators

Output format:
SEVERITY: [MILD/MODERATE/SEVERE]
REASON: [brief explanation]
DOCTOR_NEEDED: [yes/no]

Assess:
""")

chain = prompt | llm | StrOutputParser()


def assess_severity(symptoms: str) -> dict:
    """
    Analyzes symptoms and returns severity assessment.
    
    Args:
        symptoms: Refined symptoms from Agent-1
        
    Returns:
        dict with severity, reasoning, needs_doctor flag
    """
    try:
        result = chain.invoke({"symptoms": symptoms})
        
        # Parse the response
        severity = "MODERATE"  # default
        reasoning = ""
        needs_doctor = False
        
        # Extract severity level
        if "SEVERITY:" in result:
            severity_line = result.split("SEVERITY:")[1].split("\n")[0].strip()
            if "MILD" in severity_line.upper():
                severity = "MILD"
            elif "SEVERE" in severity_line.upper():
                severity = "SEVERE"
            elif "MODERATE" in severity_line.upper():
                severity = "MODERATE"
        
        # Extract reasoning
        if "REASON:" in result:
            reasoning = result.split("REASON:")[1].split("\n")[0].strip()
        
        # Determine if doctor needed
        needs_doctor = severity in ["MODERATE", "SEVERE"]
        
        return {
            "severity": severity,
            "reasoning": reasoning,
            "needs_doctor": needs_doctor,
            "raw_response": result  # Keep for debugging
        }
        
    except Exception as e:
        print(f"Severity assessment error: {e}")
        # Safe fallback - assume needs doctor if error
        return {
            "severity": "MODERATE",
            "reasoning": "Unable to assess, recommend medical consultation",
            "needs_doctor": True,
            "raw_response": ""
        }