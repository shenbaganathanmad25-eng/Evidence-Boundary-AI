from typing import List, Optional
from pydantic import BaseModel

class EBDFDeltas(BaseModel):
    delta_scope: str      # e.g., "Tested on N=450 elementary pupils in 2 schools; Claim asserts universal effect for all STEM students."
    delta_certainty: str  # e.g., "Study observes modest correlation (p=0.04); Claim asserts direct 35% causal boost."
    delta_temporal: str   # e.g., "Trial conducted over 6 months; Claim projects long-term career graduation rates."
    delta_causal: str     # e.g., "Does not isolate teacher expertise or district funding as confounding variables."

class StressTestResult(BaseModel):
    perturbation_type: str  # "SCOPE_SHIFT" | "CERTAINTY_ELEVATION" | "TEMPORAL_EXTRAPOLATION" | "CAUSAL_LEAP"
    scenario_title: str
    attack_hypothesis: str
    original_evidence_holding: str
    attacked_condition: str
    claim_survived: bool
    fragility_impact: float  # Score addition to fragility (0-25)
    breaking_point_explanation: str

class FragilityBreakdown(BaseModel):
    overall_score: float  # 0.0 (Robust) to 100.0 (Fragile / Unsupported)
    unsupported_boundary_penalty: float
    stress_test_failure_penalty: float
    ebdf_delta_penalty: float
    fragility_tier: str  # "LOW_FRAGILITY" | "MODERATE_FRAGILITY" | "HIGH_FRAGILITY" | "CRITICAL_FRAGILITY"
    explanation_summary: str
