from fastapi import APIRouter, HTTPException
from models.claim import ClaimDecompositionRequest, ClaimDecompositionResponse
from services.claim.claim_service import ClaimService

router = APIRouter(prefix="/claim", tags=["Claim Decomposition"])
claim_service = ClaimService()

@router.post("/decompose", response_model=ClaimDecompositionResponse)
def decompose_claim_endpoint(req: ClaimDecompositionRequest):
    """Decomposes a raw claim into subclaims with semantic fields and folded EBDF severities."""
    if not req.claim or not req.claim.strip():
        raise HTTPException(status_code=400, detail="Claim text is required.")

    subclaims = claim_service.decompose(req.claim)
    return ClaimDecompositionResponse(
        raw_claim=req.claim,
        subclaims=subclaims
    )
