import os
import httpx
import logging
from typing import List, Optional
from models.evidence import EvidenceItem, SupportDirectionEnum, SourceOriginEnum
from services.evidence.base_provider import BaseSearchProvider

logger = logging.getLogger("evidence_boundary.openalex_provider")

OPENALEX_API_URL = "https://api.openalex.org/works"

class OpenAlexSearchProvider(BaseSearchProvider):
    """Live academic search provider using OpenAlex Academic Graph REST API."""

    def provider_name(self) -> str:
        return "OpenAlex Academic Search Provider"

    def is_available(self) -> bool:
        return True

    def search(self, subclaim_id: str, query: str, subclaim_text: str) -> List[EvidenceItem]:
        logger.info(f"Executing LIVE search query: '{query}' for subclaim {subclaim_id}")
        results: List[EvidenceItem] = []

        try:
            with httpx.Client(timeout=8.0) as client:
                response = client.get(OPENALEX_API_URL, params={"search": query, "per_page": 2})
                if response.status_code == 200:
                    data = response.json()
                    works = data.get("results", [])

                    for idx, work in enumerate(works):
                        title = work.get("display_name", "Academic Paper")
                        year = str(work.get("publication_year", 2023))
                        doi = work.get("doi") or work.get("id", f"https://openalex.org/works/{idx}")
                        
                        primary_loc = work.get("primary_location") or {}
                        source_obj = primary_loc.get("source") or {}
                        publisher = source_obj.get("display_name") or "Academic Peer-Reviewed Journal"
                        
                        abstract_idx = work.get("abstract_inverted_index")
                        snippet = self._reconstruct_abstract(abstract_idx) or f"Empirical literature study evaluating: {query[:60]}."

                        results.append(
                            EvidenceItem(
                                id=f"ev_live_openalex_{work.get('id', idx)}",
                                subclaim_id=subclaim_id,
                                source_url=doi,
                                source_title=title,
                                publisher=publisher,
                                source_type="PEER_REVIEWED_PAPER",
                                publication_date=year,
                                passage=snippet,
                                support_direction=SupportDirectionEnum.NEUTRAL, # Unclassified initial state
                                relevance=0.88,
                                source_origin=SourceOriginEnum.LIVE
                            )
                        )
        except Exception as e:
            logger.error(f"Live OpenAlex search error: {e}")

        return results

    def _reconstruct_abstract(self, inverted_index: Optional[dict]) -> Optional[str]:
        if not inverted_index:
            return None
        try:
            word_positions = []
            for word, positions in inverted_index.items():
                for pos in positions:
                    word_positions.append((pos, word))
            word_positions.sort(key=lambda x: x[0])
            words = [w[1] for w in word_positions[:50]]
            return " ".join(words) + "..."
        except Exception:
            return None
