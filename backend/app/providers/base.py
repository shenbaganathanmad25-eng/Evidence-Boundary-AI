from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.models.claim import SubClaim
from app.models.evidence import EvidenceItem
from app.models.verdict import VerificationResponse

class BaseEvidenceProvider(ABC):
    @abstractmethod
    def fetch_evidence(self, sub_claims: List[SubClaim]) -> List[EvidenceItem]:
        pass

class BaseReasoningProvider(ABC):
    @abstractmethod
    def decompose_claim(self, raw_claim: str) -> List[SubClaim]:
        pass

    @abstractmethod
    def analyze_boundary_and_stress(
        self,
        raw_claim: str,
        sub_claims: List[SubClaim],
        evidence: List[EvidenceItem]
    ) -> Dict[str, Any]:
        pass
