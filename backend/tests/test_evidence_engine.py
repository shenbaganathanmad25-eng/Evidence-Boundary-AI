import sys
import os
import unittest

# Ensure backend root is in sys.path
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from models.claim import DecomposedSubClaim, SubClaimEBDF, EBDFItemSeverity, EBDFSeverityEnum
from models.evidence import EvidenceItem, SupportDirectionEnum, SourceOriginEnum
from services.evidence.evidence_normalizer import EvidenceNormalizer
from services.evidence.demo_provider import DemoSearchProvider
from services.evidence.openalex_provider import OpenAlexSearchProvider
from services.evidence.evidence_service import EvidenceEngine

class TestEvidenceEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EvidenceEngine()
        self.sample_subclaim = DecomposedSubClaim(
            id="sub_1",
            subclaim="AI tutoring improves student exam scores by 35%",
            entity="AI Tutoring Platform",
            subject="AI System",
            relation="Improves",
            metric="Exam Performance",
            value="35",
            unit="%",
            ebdf=SubClaimEBDF(
                scope=EBDFItemSeverity(severity=EBDFSeverityEnum.MEDIUM, explanation="Sample scope"),
                certainty=EBDFItemSeverity(severity=EBDFSeverityEnum.HIGH, explanation="Certainty boost"),
                temporal=EBDFItemSeverity(severity=EBDFSeverityEnum.LOW, explanation="Temporal window"),
                causal=EBDFItemSeverity(severity=EBDFSeverityEnum.HIGH, explanation="Causal leap")
            )
        )

    def test_query_generation(self):
        queries = self.engine.generate_targeted_queries(self.sample_subclaim)
        self.assertGreaterEqual(len(queries), 1)
        self.assertIn("AI Tutoring Platform", queries[0])

    def test_demo_evidence_retrieval(self):
        evidence_list = self.engine.gather_evidence_for_subclaims([self.sample_subclaim], force_demo=True)
        self.assertGreaterEqual(len(evidence_list), 1)
        ev = evidence_list[0]
        
        # Test required Evidence schema fields
        self.assertEqual(ev.subclaim_id, "sub_1")
        self.assertEqual(ev.source_origin, SourceOriginEnum.DEMO)
        self.assertIn(ev.support_direction, [SupportDirectionEnum.SUPPORTING, SupportDirectionEnum.CONTRADICTING, SupportDirectionEnum.NEUTRAL])
        self.assertTrue(len(ev.passage) > 10)
        self.assertIsNotNone(ev.source_title)
        self.assertIsNotNone(ev.retrieved_date)

    def test_normalization(self):
        raw_date = "May 15, 2001"
        norm_date = EvidenceNormalizer.normalize_date(raw_date)
        self.assertEqual(norm_date, "2001-05-01")

        raw_percent = "Improves scores by 35 percent and 20 %"
        norm_percent = EvidenceNormalizer.normalize_percentages_and_numbers(raw_percent)
        self.assertEqual(norm_percent, "Improves scores by 35% and 20%")

    def test_swappable_provider(self):
        # Swap provider to OpenAlex live provider explicitly
        live_engine = EvidenceEngine(provider=OpenAlexSearchProvider())
        self.assertEqual(live_engine.active_provider.provider_name(), "OpenAlex Academic Search Provider")

if __name__ == "__main__":
    unittest.main()
