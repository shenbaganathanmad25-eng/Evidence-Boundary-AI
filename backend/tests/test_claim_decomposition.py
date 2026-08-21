import sys
import os
import unittest

# Ensure backend root is in sys.path
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from services.claim.claim_service import ClaimService
from models.claim import EBDFSeverityEnum

class TestClaimDecompositionEngine(unittest.TestCase):
    def setUp(self):
        self.claim_service = ClaimService()

    def test_simple_claim_decomposition(self):
        """Test simple factual/constant claim."""
        raw_claim = "Water freezes at 0 degrees Celsius."
        subclaims = self.claim_service.decompose(raw_claim)
        
        self.assertGreaterEqual(len(subclaims), 1)
        sc = subclaims[0]
        
        self.assertEqual(sc.value, "0")
        self.assertEqual(sc.unit, "degrees Celsius")
        self.assertIn("Water", sc.entity)
        self.assertEqual(sc.ebdf.causal.severity, EBDFSeverityEnum.LOW)
        self.assertEqual(sc.ebdf.temporal.severity, EBDFSeverityEnum.LOW)

    def test_numerical_claim_decomposition(self):
        """Test numerical claim with threshold and percentage value."""
        raw_claim = "Classroom size reduction below 15 students increases math scores by 25%."
        subclaims = self.claim_service.decompose(raw_claim)
        
        self.assertGreaterEqual(len(subclaims), 1)
        sc = subclaims[0]
        
        self.assertEqual(sc.value, "15")
        self.assertIn("below 15", sc.comparison.lower())
        self.assertIsNotNone(sc.ebdf)
        self.assertIn(sc.ebdf.certainty.severity, [EBDFSeverityEnum.HIGH, EBDFSeverityEnum.MEDIUM])

    def test_causal_claim_decomposition(self):
        """Test complex causal claim with 'because' clause and percentage boost."""
        raw_claim = "AI tutoring improves student exam scores by 35% because students receive personalized feedback."
        subclaims = self.claim_service.decompose(raw_claim)
        
        # Must decompose into at least 2 subclaim clauses
        self.assertGreaterEqual(len(subclaims), 2)
        
        primary_sc = subclaims[0]
        causal_sc = subclaims[1]
        
        # Test deterministic fields
        self.assertEqual(primary_sc.value, "35")
        self.assertEqual(primary_sc.unit, "%")
        
        # Test extracted semantic fields
        self.assertIn("AI Tutoring", primary_sc.entity)
        self.assertIsNotNone(primary_sc.causal_language)
        self.assertGreater(len(primary_sc.assumptions), 0)
        
        # Test folded EBDF severity scoring
        self.assertIn(primary_sc.ebdf.causal.severity, [EBDFSeverityEnum.HIGH, EBDFSeverityEnum.VERY_HIGH])
        self.assertIn(causal_sc.ebdf.causal.severity, [EBDFSeverityEnum.HIGH, EBDFSeverityEnum.VERY_HIGH])
        self.assertTrue(len(primary_sc.ebdf.causal.explanation) > 10)

if __name__ == "__main__":
    unittest.main()
