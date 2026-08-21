from abc import ABC, abstractmethod
from typing import List
from models.evidence import EvidenceItem, SourceOriginEnum

class BaseSearchProvider(ABC):
    """Generic SearchProvider abstraction allowing pluggable search providers (Demo, OpenAlex, Semantic Scholar, Tavily, etc.)."""

    @abstractmethod
    def search(self, subclaim_id: str, query: str, subclaim_text: str) -> List[EvidenceItem]:
        """Search for candidate evidence matching a targeted query and subclaim text."""
        pass

    @abstractmethod
    def provider_name(self) -> str:
        """Return human readable provider name."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if live credentials/connections are available, False to trigger DEMO_MODE fallback."""
        pass
