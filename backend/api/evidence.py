from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from models.claim import DecomposedSubClaim
from models.evidence import EvidenceItem
from services.claim.claim_service import ClaimService
from services.evidence.evidence_service import EvidenceEngine

router = APIRouter(prefix="/evidence", tags=["Evidence Engine"])
claim_service = ClaimService()
evidence_engine = EvidenceEngine()

class EvidenceSearchRequest(BaseModel):
    claim: Optional[str] = None
    subclaims: Optional[List[DecomposedSubClaim]] = None
    force_demo: bool = False

class EvidenceSearchResponse(BaseModel):
    provider_name: str
    is_demo: bool
    evidence: List[EvidenceItem]

@router.post("/search", response_model=EvidenceSearchResponse)
def search_evidence_endpoint(req: EvidenceSearchRequest):
    """Retrieve, tag, normalize, and attach metadata to candidate evidence items for subclaims."""
    target_subclaims = req.subclaims
    if not target_subclaims and req.claim:
        target_subclaims = claim_service.decompose(req.claim)
    
    if not target_subclaims:
        raise HTTPException(status_code=400, detail="Either 'claim' or 'subclaims' list is required.")

    evidence_items = evidence_engine.gather_evidence_for_subclaims(target_subclaims, force_demo=req.force_demo)
    
    return EvidenceSearchResponse(
        provider_name=evidence_engine.active_provider.provider_name(),
        is_demo=req.force_demo or evidence_engine.active_provider.provider_name() == "Curated Demo Provider",
        evidence=evidence_items
    )
