import os
import json
import logging
from typing import Optional, Dict, Any, List
from config import settings
from database.db import log_verification
from app.models.claim import SubClaim
from models.claim import DecomposedSubClaim
from models.evidence import EvidenceItem, SupportDirectionEnum, SourceOriginEnum
from models.stress_test import EBDFDeltas, StressTestResult, FragilityBreakdown
from models.verdict import VerdictEnum, VerificationRequest, VerificationResponse
from services.claim.claim_service import ClaimService
from services.evidence.evidence_service import EvidenceEngine
from services.verification.stress_test_engine import StressTestEngine
from services.verification.fragility_calculator import FragilityCalculator

logger = logging.getLogger("evidence_boundary.verification")

class VerificationService:
    """Orchestrates full ML-driven Evidence Boundary verification pipeline and stress test execution."""

    def __init__(self):
        self.claim_service = ClaimService()
        self.evidence_engine = EvidenceEngine()
        self.stress_test_engine = StressTestEngine()

    def verify(self, request: VerificationRequest) -> VerificationResponse:
        is_demo_active = settings.DEMO_MODE or request.demo_mode
        raw_claim_text = request.claim.strip() if request.claim else "Reducing elementary classroom sizes below 15 students directly increases long-term high school STEM graduation rates by 35% across all socioeconomic demographics."
        
        logger.info(f"Processing ML verification pipeline (DEMO_MODE={is_demo_active}) for claim: '{raw_claim_text[:60]}...'")

        # 1. Decompose Claim into subclaims with folded EBDF severities
        decomp_subclaims = self.claim_service.decompose(raw_claim_text)

        # Map to SubClaim Pydantic models for response schema compatibility
        sub_claims = [
            SubClaim(
                id=sc.id,
                text=sc.subclaim,
                original_claim_segment=sc.subclaim[:50],
                is_supported=(sc.ebdf.causal.severity.value in ("LOW", "MEDIUM")),
                confidence_level=0.88 if sc.ebdf.causal.severity.value in ("LOW", "MEDIUM") else 0.35,
                boundary_gap_description=sc.ebdf.causal.explanation
            )
            for sc in decomp_subclaims
        ]

        # 2. Gather & Classify Evidence via ML model
        evidence = self.evidence_engine.gather_evidence_for_subclaims(decomp_subclaims, force_demo=is_demo_active)

        # 3. Determine EBDF Deltas
        ebdf_deltas = EBDFDeltas(
            delta_scope=decomp_subclaims[0].ebdf.scope.explanation if decomp_subclaims else "Scope over-generalization.",
            delta_certainty=decomp_subclaims[0].ebdf.certainty.explanation if decomp_subclaims else "Uncertainty elevation.",
            delta_temporal=decomp_subclaims[0].ebdf.temporal.explanation if decomp_subclaims else "Temporal extrapolation.",
            delta_causal=decomp_subclaims[0].ebdf.causal.explanation if decomp_subclaims else "Causal leap."
        )

        # 4. Assess ML Support vs Contradiction
        supporting_count = sum(1 for ev in evidence if ev.support_direction == SupportDirectionEnum.SUPPORTING)
        contradicting_count = sum(1 for ev in evidence if ev.support_direction == SupportDirectionEnum.CONTRADICTING)

        # 5. Assign Baseline Verdict
        if contradicting_count > 0:
            baseline_verdict = VerdictEnum.REFUTED
            justification = "ML Evidence Classifier identified peer-reviewed literature contradicting core claim assertions."
        elif supporting_count > 0 and len(decomp_subclaims) > 1 and any(sc.ebdf.causal.severity.value in ("HIGH", "VERY HIGH") for sc in decomp_subclaims):
            baseline_verdict = VerdictEnum.INSUFFICIENTLY_VERIFIED
            justification = "Primary premise has literature backing, but secondary assertions exceed supported empirical boundaries."
        elif supporting_count > 0:
            baseline_verdict = VerdictEnum.VERIFIED
            justification = "Claim assertions fall within empirical evidence boundaries verified by ML classification."
        else:
            baseline_verdict = VerdictEnum.INSUFFICIENTLY_VERIFIED
            justification = "Insufficient empirical evidence found to verify claim assertions."

        # Temporary preliminary fragility breakdown
        prelim_fragility = FragilityBreakdown(
            overall_score=50.0,
            unsupported_boundary_penalty=20.0,
            stress_test_failure_penalty=20.0,
            ebdf_delta_penalty=10.0,
            fragility_tier="MODERATE_FRAGILITY",
            explanation_summary="Calculating stress test suite."
        )

        # 6. Run ML Stress Suite (Test A, Test B, Test C)
        stress_suite = self.stress_test_engine.run_stress_suite(
            raw_claim=raw_claim_text,
            subclaims=decomp_subclaims,
            evidence=evidence,
            ebdf=ebdf_deltas,
            baseline_verdict=baseline_verdict,
            baseline_fragility=prelim_fragility
        )

        # 7. Calculate Deterministic 0-100 Claim Fragility Score
        frag_res = FragilityCalculator.calculate(
            subclaims=decomp_subclaims,
            evidence=evidence,
            failed_stress_tests=stress_suite["failed_tests"],
            total_stress_tests=len(stress_suite["stress_tests"])
        )

        fragility = FragilityBreakdown(
            overall_score=float(frag_res["fragility_score"]),
            unsupported_boundary_penalty=float(frag_res["breakdown"]["scope_penalty"] + frag_res["breakdown"]["causal_penalty"]),
            stress_test_failure_penalty=float(frag_res["breakdown"]["stress_penalty"]),
            ebdf_delta_penalty=float(frag_res["breakdown"]["uncertainty_penalty"]),
            fragility_tier=f"{frag_res['fragility_label']}_FRAGILITY",
            explanation_summary=frag_res["explanation"]
        )

        # Convert stress suite results into StressTestResult models
        stress_test_results = [
            StressTestResult(
                perturbation_type=t["test_name"].replace(" ", "_"),
                scenario_title=t["test_name"],
                attack_hypothesis=f"Stress attack evaluating verdict shift from {t['verdict_before']} to {t['verdict_after']}.",
                original_evidence_holding=f"Baseline Verdict: {t['verdict_before']}",
                attacked_condition=f"Post-Attack Verdict: {t['verdict_after']}",
                claim_survived=t["passed"],
                fragility_impact=20.0 if not t["passed"] else 5.0,
                breaking_point_explanation=t["explanation"]
            )
            for t in stress_suite["stress_tests"]
        ]

        response = VerificationResponse(
            claim_id="ml_verification_run",
            raw_claim=raw_claim_text,
            is_demo=is_demo_active,
            domain="Education & Domain Policy",
            sub_claims=sub_claims,
            evidence=evidence,
            ebdf_deltas=ebdf_deltas,
            stress_test_results=stress_test_results,
            fragility=fragility,
            verdict=baseline_verdict,
            verdict_justification=justification,
            boundary_summary=f"Evidence boundary established by ML Classifier. Critical failure point: {stress_suite['critical_failure_point']}",
            killer_questions=[
                "What longitudinal trial replicates the claim under strict randomized control?",
                "Are confounding socioeconomic variables disaggregated in primary literature sources?"
            ],
            missing_evidence_requirements=frag_res["critical_assumptions"],
            evidence_mutations=[
                "Observational correlation in pilot trial mutated into direct causal assertion."
            ]
        )

        # Log audit entry to SQLite
        log_verification(
            raw_claim=raw_claim_text,
            verdict=baseline_verdict.value,
            fragility_score=fragility.overall_score,
            is_demo=is_demo_active
        )

        return response
