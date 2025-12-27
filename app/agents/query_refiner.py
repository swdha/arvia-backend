from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1   # low randomness for consistent outputs
)

# Teaching Gemini to extract symptoms and mark vague inputs
prompt = ChatPromptTemplate.from_template("""
Extract medical symptoms from user input.

User input: "{user_input}"

If input is vague (like "not feeling well"), start with [VAGUE].
If specific symptoms mentioned, extract them.

Examples:
- "my head hurts" → headache
- "not feeling well" → [VAGUE] general malaise
- "stomach pain and nausea" → abdominal pain, nausea

Extract:
""")

chain = prompt | llm | StrOutputParser()


def refine_query(user_input: str) -> dict:
    try:
        result = chain.invoke({"user_input": user_input})
        
        # Check if vague
        is_vague = result.startswith("[VAGUE]")
        
        # Clean up the result
        if is_vague:
            result = result.replace("[VAGUE]", "").strip()
        
        return {
            "refined_query": result,
            "original_query": user_input,
            "needs_clarification": is_vague
        }
    except Exception as e:         # ensures system does not crash on errors
        print(f"Error: {e}")
        return {
            "refined_query": user_input,
            "original_query": user_input,
            "needs_clarification": False
        }


def extract_symptoms_structured(user_input: str) -> dict:
    refined = refine_query(user_input)
    text = refined["refined_query"]
    
    # Simple parsing   (extracting text)
    symptoms = []
    duration = None
    severity = None
    # extract duration and severity if mentioned
    if "duration:" in text:
        parts = text.split("duration:")
        symptoms_part = parts[0]
        duration = parts[1].split(",")[0].strip() if len(parts) > 1 else None
    else:
        symptoms_part = text
    
    if "severity:" in text:
        idx = text.index("severity:") + len("severity:")
        severity = text[idx:].strip()
    
    # for extracting symptoms list
    symptoms = [s.strip() for s in symptoms_part.split(",") if s.strip()]
    
    return {
        "symptoms": symptoms,
        "duration": duration,
        "severity": severity,
        "refined_query": text
    }