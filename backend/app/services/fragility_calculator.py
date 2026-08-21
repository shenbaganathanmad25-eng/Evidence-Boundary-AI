from typing import List
from app.models.claim import SubClaim
from app.models.stress_test import StressTestResult, EBDFDeltas, FragilityBreakdown

class FragilityCalculator:
    @staticmethod
    def calculate(
        sub_claims: List[SubClaim],
        stress_tests: List[StressTestResult],
        ebdf_deltas: EBDFDeltas
    ) -> FragilityBreakdown:
        if not sub_claims:
            return FragilityBreakdown(
                overall_score=50.0,
                unsupported_boundary_penalty=20.0,
                stress_test_failure_penalty=20.0,
                ebdf_delta_penalty=10.0,
                fragility_tier="MODERATE_FRAGILITY",
                explanation_summary="No subclaims provided for fragility evaluation."
            )

        # 1. Unsupported boundary ratio (0 - 40 points)
        total_subclaims = len(sub_claims)
        unsupported_count = sum(1 for sc in sub_claims if not sc.is_supported)
        unsupported_ratio = unsupported_count / total_subclaims
        boundary_penalty = round(unsupported_ratio * 40.0, 1)

        # 2. Stress test failure rate (0 - 35 points)
        if stress_tests:
            failed_tests = sum(1 for st in stress_tests if not st.claim_survived)
            failure_rate = failed_tests / len(stress_tests)
            stress_penalty = round(failure_rate * 35.0, 1)
        else:
            stress_penalty = 15.0

        # 3. EBDF Delta penalty (0 - 25 points)
        delta_penalty = 0.0
        if ebdf_deltas.delta_scope and len(ebdf_deltas.delta_scope) > 10:
            delta_penalty += 7.0
        if ebdf_deltas.delta_certainty and len(ebdf_deltas.delta_certainty) > 10:
            delta_penalty += 7.0
        if ebdf_deltas.delta_temporal and len(ebdf_deltas.delta_temporal) > 10:
            delta_penalty += 6.0
        if ebdf_deltas.delta_causal and len(ebdf_deltas.delta_causal) > 10:
            delta_penalty += 5.0
        delta_penalty = min(25.0, round(delta_penalty, 1))

        # Total Fragility Score
        overall_score = round(boundary_penalty + stress_penalty + delta_penalty, 1)
        overall_score = max(0.0, min(100.0, overall_score))

        # Assign tier
        if overall_score < 25.0:
            tier = "LOW_FRAGILITY"
            summary = "Claim is highly robust. Evidence strongly covers all asserted scope and conditions."
        elif overall_score < 55.0:
            tier = "MODERATE_FRAGILITY"
            summary = "Claim has moderate fragility. Certain boundary extrapolations require caution."
        elif overall_score < 80.0:
            tier = "HIGH_FRAGILITY"
            summary = "High fragility detected. The claim significantly exceeds supported evidence boundaries."
        else:
            tier = "CRITICAL_FRAGILITY"
            summary = "Critical fragility. Claim is largely unsupported or directly refuted under stress perturbations."

        return FragilityBreakdown(
            overall_score=overall_score,
            unsupported_boundary_penalty=boundary_penalty,
            stress_test_failure_penalty=stress_penalty,
            ebdf_delta_penalty=delta_penalty,
            fragility_tier=tier,
            explanation_summary=summary
        )
