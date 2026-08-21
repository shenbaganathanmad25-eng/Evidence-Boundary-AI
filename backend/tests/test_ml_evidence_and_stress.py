import sys
import os
import unittest

# Ensure backend root is in sys.path
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from models.claim import DecomposedSubClaim, SubClaimEBDF, EBDFItemSeverity, EBDFSeverityEnum
from models.evidence import EvidenceItem, SupportDirectionEnum, SourceOriginEnum
from app.models.verdict import VerdictEnum
from services.evidence.evidence_service import EvidenceEngine
from services.evidence.ml_passage_classifier import MLPassageClassifier
from services.verification.stress_test_engine import StressTestEngine
from services.verification.verification_service import VerificationService

class TestMLEvidenceAndStressEngine(unittest.TestCase):
    def setUp(self):
        self.evidence_engine = EvidenceEngine()
        self.ml_classifier = MLPassageClassifier()
        self.stress_engine = StressTestEngine()
        self.verification_service = VerificationService()

        self.sample_subclaim = DecomposedSubClaim(
            id="sub_1",
            subclaim="AI tutoring caused a 35% increase in exam scores",
            entity="AI Tutoring Platform",
            subject="Exam Scores",
            relation="Caused",
            metric="Exam Performance",
            value="35",
            unit="%",
            causal_language="caused",
            ebdf=SubClaimEBDF(
                scope=EBDFItemSeverity(severity=EBDFSeverityEnum.HIGH, explanation="Scope shift"),
                certainty=EBDFItemSeverity(severity=EBDFSeverityEnum.HIGH, explanation="Certainty boost"),
                temporal=EBDFItemSeverity(severity=EBDFSeverityEnum.LOW, explanation="Short trial"),
                causal=EBDFItemSeverity(severity=EBDFSeverityEnum.VERY_HIGH, explanation="Direct causality asserted")
            )
        )

    def test_ml_passage_classifier_output_format(self):
        """Test that ML classifier returns label and probabilities matching required model output shape."""
        subclaim = "AI tutoring caused a 35% increase in exam scores"
        passage = "Intelligent tutoring systems demonstrated a statistically significant 35% gain in standardized exam scores in a randomized controlled trial."
        
        result = self.ml_classifier.classify_passage(subclaim, passage)
        
        self.assertIn(result["label"], ["SUPPORTING", "CONTRADICTING", "NEUTRAL"])
        self.assertIn("SUPPORTING", result["probabilities"])
        self.assertIn("CONTRADICTING", result["probabilities"])
        self.assertIn("NEUTRAL", result["probabilities"])
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)

    def test_demo_evidence_retrieval(self):
        """Test demo evidence retrieval with ML tagging and SourceOrigin.DEMO labeling."""
        evidence_list = self.evidence_engine.gather_evidence_for_subclaims([self.sample_subclaim], force_demo=True)
        self.assertGreaterEqual(len(evidence_list), 1)
        ev = evidence_list[0]
        
        self.assertEqual(ev.source_origin, SourceOriginEnum.DEMO)
        self.assertIn(ev.support_direction, [SupportDirectionEnum.SUPPORTING, SupportDirectionEnum.CONTRADICTING, SupportDirectionEnum.NEUTRAL])

    def test_empty_result_handling(self):
        """Test that empty subclaim lists return clean empty evidence lists without crashing."""
        evidence_list = self.evidence_engine.gather_evidence_for_subclaims([])
        self.assertEqual(len(evidence_list), 0)

    def test_provider_fallback_behavior(self):
        """Test automatic fallback to DemoSearchProvider when live provider fails or force_demo is set."""
        evidence_list = self.evidence_engine.gather_evidence_for_subclaims([self.sample_subclaim], force_demo=True)
        self.assertTrue(all(ev.source_origin == SourceOriginEnum.DEMO for ev in evidence_list))

    def test_stress_test_suite_execution(self):
        """Test ML Stress Suite (Test A, Test B, Test C) output structure and verdict shift."""
        claim_text = "AI tutoring caused a 35% increase in exam scores"
        subclaims = [self.sample_subclaim]
        evidence = self.evidence_engine.gather_evidence_for_subclaims(subclaims, force_demo=True)
        
        suite_res = self.stress_engine.run_stress_suite(
            raw_claim=claim_text,
            subclaims=subclaims,
            evidence=evidence,
            ebdf=subclaims[0].ebdf,
            baseline_verdict=VerdictEnum.INSUFFICIENTLY_VERIFIED,
            baseline_fragility=self.verification_service.verify(type('Request', (), {'claim': claim_text, 'demo_mode': True})()).fragility
        )

        self.assertIn("baseline_verdict", suite_res)
        self.assertIn("stress_tests", suite_res)
        self.assertGreaterEqual(len(suite_res["stress_tests"]), 3)
        self.assertIn("failed_tests", suite_res)
        self.assertIn("passed_tests", suite_res)
        self.assertIn("fragility_score", suite_res)
        self.assertIsNotNone(suite_res["critical_failure_point"])

        # Check Test A, B, C schema
        for test in suite_res["stress_tests"]:
            self.assertIn("test_name", test)
            self.assertIn("passed", test)
            self.assertIn("verdict_before", test)
            self.assertIn("verdict_after", test)
            self.assertIn("explanation", test)

if __name__ == "__main__":
    unittest.main()
