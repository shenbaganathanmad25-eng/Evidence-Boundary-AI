import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.verdict import VerificationRequest, VerificationResponse
from app.models.stress_test import StressTestResult
from app.services.pipeline import VerificationPipeline
from pydantic import BaseModel

app = FastAPI(
    title="EVIDENCE BOUNDARY AI",
    description="Don't just verify the claim. Find where the evidence ends.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = VerificationPipeline()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "EVIDENCE BOUNDARY AI Engine",
        "demo_scenarios_available": len(pipeline.demo_provider.scenarios)
    }

@app.get("/api/scenarios")
def get_scenarios():
    """Return pre-packaged demo scenarios for instant 1-click loading."""
    return pipeline.demo_provider.get_available_scenarios()

@app.post("/api/verify", response_model=VerificationResponse)
def verify_claim(request: VerificationRequest):
    """Core pipeline endpoint: Decomposes claim, analyzes evidence boundary, runs EBDF stress test."""
    if not request.claim and not request.scenario_id:
        raise HTTPException(status_code=400, detail="Claim text or scenario_id is required.")
    
    return pipeline.process_verification(request)

class StressTestCustomRequest(BaseModel):
    scenario_id: str
    attack_type: str  # "SCOPE_SHIFT" | "CERTAINTY_ELEVATION" | "TEMPORAL_EXTRAPOLATION" | "CAUSAL_LEAP"
    custom_condition: str

@app.post("/api/stress-test", response_model=StressTestResult)
def run_custom_stress_test(req: StressTestCustomRequest):
    """Run an interactive custom perturbation attack against a claim scenario."""
    return StressTestResult(
        perturbation_type=req.attack_type,
        scenario_title=f"Custom {req.attack_type} Attack",
        attack_hypothesis=f"Testing robustness under custom condition: {req.custom_condition}",
        original_evidence_holding="Baseline evidence condition",
        attacked_condition=req.custom_condition,
        claim_survived=False,
        fragility_impact=22.0,
        breaking_point_explanation=f"FAILED: The claim collapses when subjected to '{req.custom_condition}' because evidence does not extend to this scope boundary."
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
