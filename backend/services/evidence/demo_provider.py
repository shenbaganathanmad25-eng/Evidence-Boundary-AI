import os
import json
import logging
from typing import List
from models.evidence import EvidenceItem, SupportDirectionEnum, SourceOriginEnum
from services.evidence.base_provider import BaseSearchProvider

logger = logging.getLogger("evidence_boundary.demo_provider")

DEMO_FIXTURE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "demo_data", "sample_claim.json")

class DemoSearchProvider(BaseSearchProvider):
    """Curated deterministic search provider using hardcoded demo dataset."""

    def __init__(self):
        self.fixtures = self._load_fixtures()

    def _load_fixtures(self) -> List[dict]:
        if os.path.exists(DEMO_FIXTURE_PATH):
            try:
                with open(DEMO_FIXTURE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("evidence", [])
            except Exception as e:
                logger.error(f"Failed loading demo evidence fixtures: {e}")
        return []

    def provider_name(self) -> str:
        return "Curated Demo Provider"

    def is_available(self) -> bool:
        return True

    def search(self, subclaim_id: str, query: str, subclaim_text: str) -> List[EvidenceItem]:
        text_lower = subclaim_text.lower()
        results: List[EvidenceItem] = []

        # Match from hardcoded fixtures first
        for fix in self.fixtures:
            if fix.get("sub_claim_id") == subclaim_id or subclaim_id in fix.get("sub_claim_id", ""):
                results.append(
                    EvidenceItem(
                        id=fix.get("id", f"ev_demo_{subclaim_id}"),
                        subclaim_id=subclaim_id,
                        source_url=fix.get("source_url", "https://openalex.org/works/W214589210"),
                        source_title=fix.get("source_title", "Project STAR: Longitudinal Effects of Small Class Sizes"),
                        publisher=fix.get("authors", "Krueger, A. B., & Whitmore, D. W."),
                        source_type="PEER_REVIEWED_PAPER",
                        publication_date=str(fix.get("publication_year", "2001")),
                        passage=fix.get("quote_snippet", "Students randomly assigned to small classes scored higher on math tests."),
                        support_direction=SupportDirectionEnum.NEUTRAL,  # Unclassified initial state
                        relevance=fix.get("relevance_score", 0.92),
                        source_origin=SourceOriginEnum.DEMO
                    )
                )

        if results:
            return results

        # Heuristic fallback evidence candidate
        if "water" in text_lower or "freezes" in text_lower or "celsius" in text_lower:
            return [
                EvidenceItem(
                    id=f"ev_water_{subclaim_id}",
                    subclaim_id=subclaim_id,
                    source_url="https://doi.org/10.1039/CR9620000001",
                    source_title="CRC Handbook of Chemistry and Physics: Phase Transition Constants",
                    publisher="CRC Press / Chemical Rubber Company",
                    source_type="PEER_REVIEWED_PAPER",
                    publication_date="2020-01-15",
                    passage="Pure liquid water under standard atmospheric pressure transitions to ice at precisely 0% degrees Celsius.",
                    support_direction=SupportDirectionEnum.NEUTRAL,
                    relevance=0.98,
                    source_origin=SourceOriginEnum.DEMO
                )
            ]
        elif "tutoring" in text_lower or "exam" in text_lower or "35%" in text_lower:
            return [
                EvidenceItem(
                    id=f"ev_tutoring_1_{subclaim_id}",
                    subclaim_id=subclaim_id,
                    source_url="https://openalex.org/works/W312849102",
                    source_title="Meta-Analysis of Intelligent Tutoring Systems in Secondary Education",
                    publisher="Journal of Educational Psychology",
                    source_type="PEER_REVIEWED_PAPER",
                    publication_date="2022-09-10",
                    passage="Intelligent tutoring systems demonstrated average gains of 12-15%. Meta-analysis of 40 trials found no evidence of a 35% uniform increase.",
                    support_direction=SupportDirectionEnum.NEUTRAL,
                    relevance=0.91,
                    source_origin=SourceOriginEnum.DEMO
                )
            ]
        else:
            return [
                EvidenceItem(
                    id=f"ev_generic_{subclaim_id}",
                    subclaim_id=subclaim_id,
                    source_url="https://openalex.org/works/W000000000",
                    source_title="Empirical Assessment of Domain Hypotheses",
                    publisher="Journal of Evidentiary Analysis",
                    source_type="PEER_REVIEWED_PAPER",
                    publication_date="2023-06-01",
                    passage=f"Controlled study evaluated initial premise of: '{subclaim_text[:60]}...' and found partial supporting correlation.",
                    support_direction=SupportDirectionEnum.NEUTRAL,
                    relevance=0.85,
                    source_origin=SourceOriginEnum.DEMO
                )
            ]
