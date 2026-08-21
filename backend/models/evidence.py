from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class SupportDirectionEnum(str, Enum):
    SUPPORTING = "SUPPORTING"
    CONTRADICTING = "CONTRADICTING"
    NEUTRAL = "NEUTRAL"

class SourceOriginEnum(str, Enum):
    DEMO = "DEMO"
    LIVE = "LIVE"

class EvidenceItem(BaseModel):
    id: str
    subclaim_id: str
    source_url: Optional[str] = None
    source_title: str
    publisher: Optional[str] = "Academic Journal / Domain Index"
    source_type: str = "PEER_REVIEWED_PAPER"
    publication_date: Optional[str] = "2023"
    retrieved_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    passage: str
    support_direction: SupportDirectionEnum = SupportDirectionEnum.SUPPORTING
    relevance: float = 0.85
    source_origin: SourceOriginEnum = SourceOriginEnum.DEMO
