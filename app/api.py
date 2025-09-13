from fastapi import FastAPI
from pydantic import BaseModel
from app.model import BertModel

app = FastAPI(title="BERTimbau Fine-tuned API")

# Carregar o modelo
model = BertModel()

class PredictionRequest(BaseModel):
    text: str
    max_length: int = 512

class PredictionResponse(BaseModel):
    class_id: int
    class_name: str
    probabilities: list

@app.get("/")
async def root():
    return {"message": "BERTimbau Fine-tuned API"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    result = model.predict(request.text, request.max_length)
    return {
        "class_name": result["class"],
        "class_id": result["class_id"],
        "probabilities": result["probabilities"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}