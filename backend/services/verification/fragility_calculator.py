from typing import List, Dict, Any
from models.claim import DecomposedSubClaim
from models.evidence import EvidenceItem, SupportDirectionEnum
from models.stress_test import FragilityBreakdown

class FragilityCalculator:
    """Deterministic, reproducible Claim Fragility Scoring engine (0 - 100) with zero randomness."""

    @staticmethod
    def calculate(
        subclaims: List[DecomposedSubClaim],
        evidence: List[EvidenceItem],
        failed_stress_tests: int,
        total_stress_tests: int
    ) -> Dict[str, Any]:
        if not subclaims:
            return {
                "fragility_score": 50,
                "fragility_label": "MEDIUM",
                "critical_assumptions": ["Baseline evidence availability"],
                "explanation": "No subclaims provided for fragility evaluation."
            }

        # 1. Stress-test failures (0–40 pts)
        stress_ratio = (failed_stress_tests / max(1, total_stress_tests))
        stress_penalty = round(stress_ratio * 40.0)

        # 2. Evidence balance ratio (0–25 pts)
        supporting_count = sum(1 for ev in evidence if ev.support_direction == SupportDirectionEnum.SUPPORTING)
        contradicting_count = sum(1 for ev in evidence if ev.support_direction == SupportDirectionEnum.CONTRADICTING)
        
        if supporting_count == 0 and contradicting_count == 0:
            evidence_penalty = 20
        else:
            evidence_penalty = round((contradicting_count / (supporting_count + contradicting_count + 1)) * 25.0)

        # 3. Causal weakness from EBDF (0–15 pts)
        causal_severities = [sc.ebdf.causal.severity.value for sc in subclaims if hasattr(sc, 'ebdf')]
        if "VERY HIGH" in causal_severities or "VERY_HIGH" in causal_severities:
            causal_penalty = 15
        elif "HIGH" in causal_severities:
            causal_penalty = 10
        elif "MEDIUM" in causal_severities:
            causal_penalty = 5
        else:
            causal_penalty = 0

        # 4. Scope weakness from EBDF (0–10 pts)
        scope_severities = [sc.ebdf.scope.severity.value for sc in subclaims if hasattr(sc, 'ebdf')]
        if "VERY HIGH" in scope_severities or "VERY_HIGH" in scope_severities:
            scope_penalty = 10
        elif "HIGH" in scope_severities:
            scope_penalty = 7
        elif "MEDIUM" in scope_severities:
            scope_penalty = 3
        else:
            scope_penalty = 0

        # 5. ML Uncertainty (0–10 pts)
        if evidence:
            avg_relevance = sum(ev.relevance for ev in evidence) / len(evidence)
            uncertainty_penalty = round((1.0 - avg_relevance) * 10.0)
        else:
            uncertainty_penalty = 8

        # Total Fragility Score (0–100)
        total_score = stress_penalty + evidence_penalty + causal_penalty + scope_penalty + uncertainty_penalty
        total_score = max(0, min(100, total_score))

        # Assign label: 0–30 LOW, 31–60 MEDIUM, 61–100 HIGH
        if total_score <= 30:
            label = "LOW"
        elif total_score <= 60:
            label = "MEDIUM"
        else:
            label = "HIGH"

        # Critical assumptions extraction
        critical_assumptions = []
        if causal_penalty >= 10:
            critical_assumptions.append("Direct Causality")
        if scope_penalty >= 7:
            critical_assumptions.append("Population Scope")
        if evidence_penalty >= 10:
            critical_assumptions.append("Controlled Comparison")
        if stress_penalty >= 20:
            critical_assumptions.append("Intervention Durability")

        if not critical_assumptions:
            critical_assumptions = ["Baseline Domain Conditions"]

        explanation = (
            f"Fragility score {total_score}/100 ({label} risk). "
            f"Key drivers: {failed_stress_tests}/{total_stress_tests} stress test failures (+{stress_penalty} pts), "
            f"EBDF causal weakness (+{causal_penalty} pts), scope over-extension (+{scope_penalty} pts)."
        )

        return {
            "fragility_score": total_score,
            "fragility_label": label,
            "critical_assumptions": critical_assumptions,
            "explanation": explanation,
            "breakdown": {
                "stress_penalty": stress_penalty,
                "evidence_penalty": evidence_penalty,
                "causal_penalty": causal_penalty,
                "scope_penalty": scope_penalty,
                "uncertainty_penalty": uncertainty_penalty
            }
        }
