from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from app.models.claim import SubClaim
from app.models.evidence import EvidenceItem
from app.models.stress_test import EBDFDeltas, StressTestResult, FragilityBreakdown

class VerdictEnum(str, Enum):
    VERIFIED = "VERIFIED"
    INSUFFICIENTLY_VERIFIED = "INSUFFICIENTLY_VERIFIED"
    REFUTED = "REFUTED"

class VerificationRequest(BaseModel):
    claim: str
    demo_mode: bool = True
    scenario_id: Optional[str] = None

class VerificationResponse(BaseModel):
    claim_id: str
    raw_claim: str
    is_demo: bool
    domain: str
    sub_claims: List[SubClaim]
    evidence: List[EvidenceItem]
    ebdf_deltas: EBDFDeltas
    stress_test_results: List[StressTestResult]
    fragility: FragilityBreakdown
    verdict: VerdictEnum
    verdict_justification: str
    boundary_summary: str
    # P1 Extensions
    killer_questions: Optional[List[str]] = None
    missing_evidence_requirements: Optional[List[str]] = None
    evidence_mutations: Optional[List[str]] = None
