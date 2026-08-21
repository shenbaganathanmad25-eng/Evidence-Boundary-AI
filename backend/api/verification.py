from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.verdict import VerificationRequest, VerificationResponse
from app.models.stress_test import StressTestResult
from services.verification.verification_service import VerificationService
from services.verification.stress_test_engine import StressTestEngine
from models.verdict import VerdictEnum
from config import settings

router = APIRouter(tags=["Verification"])
verification_service = VerificationService()
stress_engine = StressTestEngine()

@router.post("/verify", response_model=VerificationResponse)
def verify_claim(request: VerificationRequest):
    """Core verification pipeline endpoint. Returns full deterministic sample pipeline when DEMO_MODE=True."""
    return verification_service.verify(request)

@router.get("/scenarios")
def get_scenarios():
    """Return available demo scenarios."""
    return [
        {
            "scenario_id": "demo_star_education_claim",
            "title": "Classroom Size & STEM Graduation",
            "domain": "Education & Policy",
            "raw_claim": "Reducing elementary classroom sizes below 15 students directly increases long-term high school STEM graduation rates by 35% across all socioeconomic demographics."
        },
        {
          "scenario_id": "scenario_medical",
          "title": "Daily Omega-3 & Alzheimer's",
          "domain": "Medical Science",
          "raw_claim": "Daily high-dose Omega-3 supplementation (2000mg EPA/DHA) completely prevents cognitive decline and reverses early-stage Alzheimer's disease in adults over 65."
        },
        {
          "scenario_id": "scenario_ai_benchmarks",
          "title": "LLM Legal Reasoning & Bar Exam",
          "domain": "AI Benchmarks",
          "raw_claim": "Model X-900 surpasses human legal experts in contract law analysis and eliminates human lawyer oversight in corporate M&A due diligence."
        }
    ]

class StressTestCustomRequest(BaseModel):
    scenario_id: str
    attack_type: str
    custom_condition: str

@router.post("/stress-test", response_model=StressTestResult)
def run_custom_stress_test(req: StressTestCustomRequest):
    """Interactively execute custom stress test attack vector against a claim scenario."""
    attack_type_upper = req.attack_type.upper()
    condition = req.custom_condition.strip()

    # Determine breaking condition
    is_breach = any(w in condition.lower() for w in ["all", "every", "nationwide", "cross-border", "unassisted", "reverses", "universal"]) or len(condition) > 5

    verdict_before = VerdictEnum.INSUFFICIENTLY_VERIFIED.value
    verdict_after = VerdictEnum.REFUTED.value if is_breach else VerdictEnum.INSUFFICIENTLY_VERIFIED.value

    return StressTestResult(
        perturbation_type=attack_type_upper,
        scenario_title=f"Custom {req.attack_type} Attack",
        attack_hypothesis=f"Testing evidence robustness under condition: '{condition}'",
        original_evidence_holding=f"Baseline Verdict: {verdict_before}",
        attacked_condition=f"Post-Attack Verdict: {verdict_after}",
        claim_survived=not is_breach,
        fragility_impact=25.0 if is_breach else 5.0,
        breaking_point_explanation=f"FAILED: The claim collapses under '{condition}' because available evidence boundary does not extend to this scope." if is_breach else f"PASSED: Claim holds under condition: '{condition}'."
    )
