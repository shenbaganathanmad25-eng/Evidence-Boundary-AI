import os
import json
from typing import List, Dict, Any, Optional
from app.models.claim import SubClaim
from app.models.evidence import EvidenceItem
from app.models.stress_test import EBDFDeltas, StressTestResult, FragilityBreakdown
from app.models.verdict import VerdictEnum, VerificationResponse
from app.providers.base import BaseEvidenceProvider, BaseReasoningProvider

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

class DemoProvider(BaseEvidenceProvider, BaseReasoningProvider):
    def __init__(self):
        self.scenarios: Dict[str, Dict[str, Any]] = {}
        self.load_scenarios()

    def load_scenarios(self):
        if not os.path.exists(DATA_DIR):
            return
        for fname in os.listdir(DATA_DIR):
            if fname.endswith(".json"):
                path = os.path.join(DATA_DIR, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        sid = data.get("scenario_id")
                        if sid:
                            self.scenarios[sid] = data
                except Exception as e:
                    print(f"Error loading scenario {fname}: {e}")

    def get_available_scenarios(self) -> List[Dict[str, Any]]:
        return [
            {
                "scenario_id": s["scenario_id"],
                "title": s["title"],
                "domain": s["domain"],
                "raw_claim": s["raw_claim"]
            }
            for s in self.scenarios.values()
        ]

    def match_scenario(self, raw_claim: str, scenario_id: Optional[str] = None) -> Dict[str, Any]:
        if scenario_id and scenario_id in self.scenarios:
            return self.scenarios[scenario_id]

        text_lower = raw_claim.lower()
        if "class" in text_lower or "stem" in text_lower or "school" in text_lower or "student" in text_lower:
            return self.scenarios.get("scenario_education", list(self.scenarios.values())[0])
        elif "omega" in text_lower or "alzheimer" in text_lower or "dementia" in text_lower or "medical" in text_lower:
            return self.scenarios.get("scenario_medical", list(self.scenarios.values())[0])
        elif "model" in text_lower or "bar" in text_lower or "law" in text_lower or "llm" in text_lower or "ai" in text_lower:
            return self.scenarios.get("scenario_ai_benchmarks", list(self.scenarios.values())[0])

        # Default fallback scenario
        return list(self.scenarios.values())[0] if self.scenarios else self._dynamic_fallback_scenario(raw_claim)

    def fetch_evidence(self, sub_claims: List[SubClaim]) -> List[EvidenceItem]:
        # Satisfied within match_scenario / full verification pipeline
        return []

    def decompose_claim(self, raw_claim: str) -> List[SubClaim]:
        scenario = self.match_scenario(raw_claim)
        return [SubClaim(**sc) for sc in scenario["sub_claims"]]

    def analyze_boundary_and_stress(
        self,
        raw_claim: str,
        sub_claims: List[SubClaim],
        evidence: List[EvidenceItem]
    ) -> Dict[str, Any]:
        scenario = self.match_scenario(raw_claim)
        return scenario

    def build_verification_response(self, raw_claim: str, scenario_id: Optional[str] = None) -> VerificationResponse:
        s = self.match_scenario(raw_claim, scenario_id)
        
        sub_claims = [SubClaim(**sc) for sc in s["sub_claims"]]
        evidence = [EvidenceItem(**ev) for ev in s["evidence"]]
        ebdf = EBDFDeltas(**s["ebdf_deltas"])
        stress_tests = [StressTestResult(**st) for st in s["stress_test_results"]]
        fragility = FragilityBreakdown(**s["fragility"])

        return VerificationResponse(
            claim_id=s["scenario_id"],
            raw_claim=raw_claim if scenario_id is None else s["raw_claim"],
            is_demo=True,
            domain=s.get("domain", "General"),
            sub_claims=sub_claims,
            evidence=evidence,
            ebdf_deltas=ebdf,
            stress_test_results=stress_tests,
            fragility=fragility,
            verdict=VerdictEnum(s["verdict"]),
            verdict_justification=s["verdict_justification"],
            boundary_summary=s["boundary_summary"],
            killer_questions=s.get("killer_questions", []),
            missing_evidence_requirements=s.get("missing_evidence_requirements", []),
            evidence_mutations=s.get("evidence_mutations", [])
        )

    def _dynamic_fallback_scenario(self, raw_claim: str) -> Dict[str, Any]:
        return {
            "scenario_id": "custom_claim_demo",
            "title": "Custom User Claim Analysis",
            "domain": "General Domain",
            "raw_claim": raw_claim,
            "sub_claims": [
                {
                    "id": "sub_1",
                    "text": f"Core observable premise of: {raw_claim[:60]}...",
                    "original_claim_segment": raw_claim[:40],
                    "is_supported": True,
                    "confidence_level": 0.85,
                    "boundary_gap_description": "Supported under controlled initial conditions."
                },
                {
                    "id": "sub_2",
                    "text": "Generalization across broader populations and extended durations.",
                    "original_claim_segment": "extended impact",
                    "is_supported": False,
                    "confidence_level": 0.30,
                    "boundary_gap_description": "UNSUPPORTED BOUNDARY GAP: Insufficient empirical data for broad scaling."
                }
            ],
            "evidence": [
                {
                    "id": "ev_1",
                    "sub_claim_id": "sub_1",
                    "source_title": "Empirical Review of Claims in General Domain Literature",
                    "authors": "Journal of Evidentiary Analysis",
                    "publication_year": 2024,
                    "quote_snippet": "Initial trials demonstrate partial positive correlation under controlled settings.",
                    "evidence_type": "SUPPORTING",
                    "relevance_score": 0.88,
                    "sample_size": "N = 150",
                    "is_demo": True
                }
            ],
            "ebdf_deltas": {
                "delta_scope": "Sample scope is restricted; claim over-generalizes to universal applicability.",
                "delta_certainty": "Source indicates potential association; claim asserts definitive cause.",
                "delta_temporal": "Evaluation timeframe was 30 days; claim projects long-term permanence.",
                "delta_causal": "Fails to control for secondary environmental variables."
            },
            "stress_test_results": [
                {
                    "perturbation_type": "SCOPE_SHIFT",
                    "scenario_title": "Population Generalization Attack",
                    "attack_hypothesis": "Test performance under altered target demographic conditions.",
                    "original_evidence_holding": "Valid under narrow controlled conditions.",
                    "attacked_condition": "Broad public deployment.",
                    "claim_survived": False,
                    "fragility_impact": 25.0,
                    "breaking_point_explanation": "FAILED: Evidence does not support generalization beyond initial sample."
                }
            ],
            "fragility": {
                "overall_score": 68.0,
                "unsupported_boundary_penalty": 30.0,
                "stress_test_failure_penalty": 25.0,
                "ebdf_delta_penalty": 13.0,
                "fragility_tier": "HIGH_FRAGILITY",
                "explanation_summary": "Claim goes beyond available baseline evidence."
            },
            "verdict": "INSUFFICIENTLY_VERIFIED",
            "verdict_justification": "Initial premise has partial support, but broad claim elements exceed available evidence.",
            "boundary_summary": "Evidence boundary ends at controlled short-term sample observation.",
            "killer_questions": ["What long-term trial supports this claim?", "How are confounding factors isolated?"],
            "missing_evidence_requirements": ["Randomized controlled trial over 12 months.", "Independent replication study."],
            "evidence_mutations": ["Correlation in pilot trial converted into absolute assertion."]
        }
