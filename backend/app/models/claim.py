from typing import List, Optional
from pydantic import BaseModel, Field

class SubClaim(BaseModel):
    id: str
    text: str
    original_claim_segment: str
    is_supported: bool
    confidence_level: float  # 0.0 to 1.0
    boundary_gap_description: Optional[str] = None

class Claim(BaseModel):
    id: str
    raw_text: str
    domain: str = "General"
    sub_claims: List[SubClaim] = []
