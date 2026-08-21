from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class EBDFSeverityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY HIGH"

class EBDFItemSeverity(BaseModel):
    severity: EBDFSeverityEnum
    explanation: str

class SubClaimEBDF(BaseModel):
    scope: EBDFItemSeverity
    certainty: EBDFItemSeverity
    temporal: EBDFItemSeverity
    causal: EBDFItemSeverity

class DecomposedSubClaim(BaseModel):
    id: str
    subclaim: str
    entity: Optional[str] = "Unspecified"
    subject: Optional[str] = "Unspecified"
    relation: Optional[str] = "Unspecified"
    metric: Optional[str] = "Unspecified"
    value: Optional[str] = "Unspecified"
    unit: Optional[str] = "Unspecified"
    time: Optional[str] = "Unspecified"
    geography: Optional[str] = "Unspecified"
    population: Optional[str] = "Unspecified"
    scope: Optional[str] = "Unspecified"
    certainty: Optional[str] = "Unspecified"
    causal_language: Optional[str] = "Unspecified"
    comparison: Optional[str] = "Unspecified"
    assumptions: List[str] = Field(default_factory=list)
    ebdf: SubClaimEBDF

class ClaimDecompositionRequest(BaseModel):
    claim: str

class ClaimDecompositionResponse(BaseModel):
    raw_claim: str
    subclaims: List[DecomposedSubClaim]
