import re
from typing import Optional
from models.evidence import EvidenceItem

class EvidenceNormalizer:
    """Normalizes date formats and number/percentage expressions in evidence data."""

    MONTH_MAP = {
        "january": "01", "jan": "01",
        "february": "02", "feb": "02",
        "march": "03", "mar": "03",
        "april": "04", "apr": "04",
        "may": "05",
        "june": "06", "jun": "06",
        "july": "07", "jul": "07",
        "august": "08", "aug": "08",
        "september": "09", "sep": "09", "sept": "09",
        "october": "10", "oct": "10",
        "november": "11", "nov": "11",
        "december": "12", "dec": "12"
    }

    @classmethod
    def normalize_date(cls, raw_date: Optional[str]) -> str:
        if not raw_date:
            return "2023"
        
        date_str = str(raw_date).strip()

        # Match YYYY-MM-DD
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str

        # Match YYYY
        year_match = re.search(r'\b(19\d\d|20\d\d)\b', date_str)
        if year_match:
            year = year_match.group(1)
            # Try finding month
            for m_name, m_num in cls.MONTH_MAP.items():
                if m_name in date_str.lower():
                    return f"{year}-{m_num}-01"
            return year

        return date_str

    @classmethod
    def normalize_percentages_and_numbers(cls, text: str) -> str:
        if not text:
            return ""
        
        # Replace "35 percent" or "35 Percent" with "35%"
        text = re.sub(r'(\d+(?:\.\d+)?)\s*percent\b', r'\1%', text, flags=re.IGNORECASE)
        # Standardize "35 %" to "35%"
        text = re.sub(r'(\d+(?:\.\d+)?)\s+%', r'\1%', text)
        return text

    @classmethod
    def normalize(cls, item: EvidenceItem) -> EvidenceItem:
        item.publication_date = cls.normalize_date(item.publication_date)
        item.passage = cls.normalize_percentages_and_numbers(item.passage)
        item.source_title = cls.normalize_percentages_and_numbers(item.source_title)
        return item
