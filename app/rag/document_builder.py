# preparing the knowledge base documents
from langchain_core.documents import Document
from app.data.symptom_data import SYMPTOM_DB

# converts to langchain Document format
def build_documents():
    docs = []

    for symptom, info in SYMPTOM_DB.items():
        text = (
            f"Symptom: {symptom}. "
            f"Possible causes: {', '.join(info['possible_causes'])}. "
            f"Recommended doctor: {info['doctor']}. "
            f"Self care tips: {', '.join(info['self_care'])}."
        )

        doc = Document(
            page_content=text,
            metadata={ #(not embedded, attached info)
                "symptom": symptom,
                "doctor": info["doctor"]
            }
        )

        docs.append(doc)

    return docs
