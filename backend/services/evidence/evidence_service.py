import re
import logging
from typing import List, Optional
from config import settings
from models.claim import DecomposedSubClaim
from models.evidence import EvidenceItem, SupportDirectionEnum, SourceOriginEnum
from services.evidence.base_provider import BaseSearchProvider
from services.evidence.demo_provider import DemoSearchProvider
from services.evidence.openalex_provider import OpenAlexSearchProvider
from services.evidence.evidence_normalizer import EvidenceNormalizer
from services.evidence.ml_passage_classifier import MLPassageClassifier

logger = logging.getLogger("evidence_boundary.evidence_service")

class EvidenceEngine:
    """Evidence Engine orchestrator managing deterministic NLP query generation, search provider execution, and ML evidence classification."""

    def __init__(self, provider: Optional[BaseSearchProvider] = None):
        self.demo_provider = DemoSearchProvider()
        self.live_provider = OpenAlexSearchProvider()
        self.active_provider = provider or (self.demo_provider if settings.DEMO_MODE else self.live_provider)
        self.ml_classifier = MLPassageClassifier()

    def generate_targeted_queries(self, subclaim: DecomposedSubClaim) -> List[str]:
        """Generates multiple targeted search queries using deterministic NLP from subclaim attributes (no LLM)."""
        queries: List[str] = []
        text = subclaim.subclaim
        entity = subclaim.entity if subclaim.entity and subclaim.entity != "Unspecified" else ""
        metric = subclaim.metric if subclaim.metric and subclaim.metric != "Unspecified" else ""
        population = subclaim.population if subclaim.population and subclaim.population != "Unspecified" else ""
        val = subclaim.value if subclaim.value and subclaim.value != "Unspecified" else ""
        unit = subclaim.unit if subclaim.unit and subclaim.unit != "Unspecified" else ""

        # 1. Primary entity + metric query
        if entity and metric:
            queries.append(f"{entity} {metric}".strip())

        # 2. Entity + population query
        if entity and population:
            queries.append(f"{entity} {population}".strip())

        # 3. Entity + numeric value query
        if entity and val:
            queries.append(f"{entity} {val}{unit} {metric}".strip())

        # 4. Causal effect query
        if subclaim.causal_language and subclaim.causal_language != "None":
            queries.append(f"{entity} causal effect student scores".strip())

        # Fallback if no specific attributes extracted
        if not queries:
            clean = re.sub(r'[^\w\s]', '', text)
            words = [w for w in clean.split() if len(w) > 3 and w.lower() not in ("because", "students", "improves")]
            queries.append(" ".join(words[:4]) if words else text[:60])

        return queries

    def gather_evidence_for_subclaims(
        self,
        subclaims: List[DecomposedSubClaim],
        force_demo: bool = False
    ) -> List[EvidenceItem]:
        """Gathers, classifies via ML, normalizes, and attaches metadata to evidence items for subclaims."""
        all_evidence: List[EvidenceItem] = []
        is_demo_run = settings.DEMO_MODE or force_demo or not self.active_provider.is_available()
        provider_to_use = self.demo_provider if is_demo_run else self.active_provider

        logger.info(f"Evidence Engine retrieving via: {provider_to_use.provider_name()} (is_demo={is_demo_run})")

        for sc in subclaims:
            queries = self.generate_targeted_queries(sc)
            primary_query = queries[0]
            
            try:
                raw_items = provider_to_use.search(sc.id, primary_query, sc.subclaim)
            except Exception as e:
                logger.error(f"Search provider failed for subclaim {sc.id}: {e}. Falling back to DemoProvider.")
                raw_items = self.demo_provider.search(sc.id, primary_query, sc.subclaim)

            # Classify candidate evidence passages using ML model
            for item in raw_items:
                ml_res = self.ml_classifier.classify_passage(sc.subclaim, item.passage)
                pred_label = ml_res["label"]

                # Assign ML classification label
                item.support_direction = SupportDirectionEnum(pred_label)
                item.relevance = ml_res["confidence"]

                # Normalize text and date formats
                normalized_item = EvidenceNormalizer.normalize(item)
                normalized_item.source_origin = SourceOriginEnum.DEMO if is_demo_run else SourceOriginEnum.LIVE
                
                all_evidence.append(normalized_item)

        return all_evidence
