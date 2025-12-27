from fastapi import FastAPI
from app.routes.symptom import router as symptom_router

app = FastAPI()

@app.get("/")
def health():
    return {"status": "backend alive"}

app.include_router(symptom_router)
