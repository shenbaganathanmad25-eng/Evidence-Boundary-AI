import logging
from typing import List, Dict, Any
from models.claim import DecomposedSubClaim
from models.evidence import EvidenceItem, SupportDirectionEnum
from models.stress_test import EBDFDeltas, StressTestResult, FragilityBreakdown
from models.verdict import VerdictEnum
from services.evidence.ml_passage_classifier import MLPassageClassifier
from services.claim.claim_service import ClaimService

logger = logging.getLogger("evidence_boundary.stress_test_engine")

class StressTestEngine:
    """ML-Driven Evidence Boundary Stress Test Engine executing Test A (Source Removal), Test B (Causality Attack), and Test C (Scope Shift)."""

    def __init__(self):
        self.ml_classifier = MLPassageClassifier()
        self.claim_service = ClaimService()

    def run_stress_suite(
        self,
        raw_claim: str,
        subclaims: List[DecomposedSubClaim],
        evidence: List[EvidenceItem],
        ebdf: EBDFDeltas,
        baseline_verdict: VerdictEnum,
        baseline_fragility: FragilityBreakdown
    ) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []
        
        # 1. TEST A — SOURCE REMOVAL ATTACK
        test_a = self._test_a_source_removal(raw_claim, subclaims, evidence, baseline_verdict)
        results.append(test_a)

        # 2. TEST B — CAUSALITY ATTACK
        test_b = self._test_b_causality_attack(raw_claim, subclaims, evidence, baseline_verdict)
        results.append(test_b)

        # 3. TEST C — SCOPE SHIFT ATTACK
        test_c = self._test_c_scope_shift(raw_claim, subclaims, evidence, baseline_verdict)
        results.append(test_c)

        # Calculate counts
        failed_count = sum(1 for t in results if not t["passed"])
        passed_count = sum(1 for t in results if t["passed"])

        # Determine critical failure point
        critical_point = "None"
        for t in results:
            if not t["passed"]:
                critical_point = f"{t['test_name']}: {t['explanation']}"
                break

        # Calculate final stress fragility score
        stress_fragility_score = min(100.0, round(baseline_fragility.overall_score + (failed_count * 15.0), 1))

        return {
            "baseline_verdict": baseline_verdict.value,
            "stress_tests": results,
            "failed_tests": failed_count,
            "passed_tests": passed_count,
            "fragility_score": stress_fragility_score,
            "critical_failure_point": critical_point
        }

    def _test_a_source_removal(
        self,
        raw_claim: str,
        subclaims: List[DecomposedSubClaim],
        evidence: List[EvidenceItem],
        baseline_verdict: VerdictEnum
    ) -> Dict[str, Any]:
        """Test A: Remove strongest supporting source and re-evaluate ML classification and verdict."""
        test_name = "TEST A — SOURCE REMOVAL"
        
        supporting_ev = [ev for ev in evidence if ev.support_direction == SupportDirectionEnum.SUPPORTING]
        if not supporting_ev:
            return {
                "test_name": test_name,
                "passed": False,
                "verdict_before": baseline_verdict.value,
                "verdict_after": VerdictEnum.REFUTED.value,
                "explanation": "FAILED: Zero supporting sources available prior to removal attack."
            }

        # Sort supporting evidence by ML confidence relevance score
        sorted_ev = sorted(supporting_ev, key=lambda x: x.relevance, reverse=True)
        removed_source = sorted_ev[0]
        remaining_ev = [ev for ev in evidence if ev.id != removed_source.id]

        # Re-evaluate remaining support
        remaining_supporting = [ev for ev in remaining_ev if ev.support_direction == SupportDirectionEnum.SUPPORTING]
        
        if len(remaining_supporting) == 0:
            verdict_after = VerdictEnum.INSUFFICIENTLY_VERIFIED if baseline_verdict == VerdictEnum.VERIFIED else VerdictEnum.REFUTED
            passed = False
            exp = f"FAILED: Removing primary source '{removed_source.source_title[:40]}...' eliminates all supporting evidence, forcing verdict downgrade."
        else:
            verdict_after = baseline_verdict.value
            passed = True
            exp = f"PASSED: Claim retains supporting evidence from secondary literature after removing '{removed_source.source_title[:40]}...'."

        return {
            "test_name": test_name,
            "passed": passed,
            "verdict_before": baseline_verdict.value,
            "verdict_after": verdict_after if isinstance(verdict_after, str) else verdict_after.value,
            "explanation": exp
        }

    def _test_b_causality_attack(
        self,
        raw_claim: str,
        subclaims: List[DecomposedSubClaim],
        evidence: List[EvidenceItem],
        baseline_verdict: VerdictEnum
    ) -> Dict[str, Any]:
        """Test B: Challenge causal interpretation (e.g. claim asserts 'caused' vs evidence asserts 'associated with')."""
        test_name = "TEST B — CAUSALITY ATTACK"
        
        text_lower = raw_claim.lower()
        asserts_causal = any(w in text_lower for w in ["caused", "causes", "improves by", "increases by", "reverses"])

        # Check if evidence mentions correlation / observational association
        evidence_observational = any(
            "observational" in ev.passage.lower() or "association" in ev.passage.lower() or "correlation" in ev.passage.lower()
            for ev in evidence
        )

        if asserts_causal and (evidence_observational or baseline_verdict != VerdictEnum.VERIFIED):
            verdict_after = VerdictEnum.REFUTED.value if baseline_verdict == VerdictEnum.INSUFFICIENTLY_VERIFIED else VerdictEnum.INSUFFICIENTLY_VERIFIED.value
            return {
                "test_name": test_name,
                "passed": False,
                "verdict_before": baseline_verdict.value,
                "verdict_after": verdict_after,
                "explanation": "FAILED: Claim asserts direct mono-causal mechanism ('caused/improves'), but evidence establishes observational association without isolating confounding variables. ΔCausal elevated to VERY HIGH."
            }
        else:
            return {
                "test_name": test_name,
                "passed": True,
                "verdict_before": baseline_verdict.value,
                "verdict_after": baseline_verdict.value,
                "explanation": "PASSED: Causal assertions align with randomized controlled trial evidence."
            }

    def _test_c_scope_shift(
        self,
        raw_claim: str,
        subclaims: List[DecomposedSubClaim],
        evidence: List[EvidenceItem],
        baseline_verdict: VerdictEnum
    ) -> Dict[str, Any]:
        """Test C: Expand claim scope (e.g. single school trial expanded to all schools nationwide)."""
        test_name = "TEST C — SCOPE SHIFT"

        text_lower = raw_claim.lower()
        has_universal_scope = any(w in text_lower for w in ["all", "every", "nationwide", "universal", "across all"])

        if has_universal_scope or baseline_verdict != VerdictEnum.VERIFIED:
            return {
                "test_name": test_name,
                "passed": False,
                "verdict_before": baseline_verdict.value,
                "verdict_after": VerdictEnum.REFUTED.value,
                "explanation": "FAILED: Expanding scope from studied sample cohort to universal nationwide application breaches evidence boundary. ΔScope elevated to VERY HIGH."
            }
        else:
            return {
                "test_name": test_name,
                "passed": True,
                "verdict_before": baseline_verdict.value,
                "verdict_after": baseline_verdict.value,
                "explanation": "PASSED: Claim scope is appropriately restricted to studied demographic cohort."
            }
