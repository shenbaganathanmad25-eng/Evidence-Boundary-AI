from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from predict import predict

router = APIRouter(tags=["ML Prediction"])

class PredictRequest(BaseModel):
    claim: str
    evidence: str

class PredictResponse(BaseModel):
    prediction: str
    confidence: float
    model_version: str
    similarity_score: float

@router.post("/predict", response_model=PredictResponse)
def predict_endpoint(req: PredictRequest):
    """FastAPI endpoint executing ML Evidence Verification prediction."""
    if not req.claim.strip() or not req.evidence.strip():
        raise HTTPException(status_code=400, detail="Claim and evidence text must not be empty.")
    
    return predict(req.claim, req.evidence)

@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
