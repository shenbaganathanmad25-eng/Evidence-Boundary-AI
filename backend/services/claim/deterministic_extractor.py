import re
from typing import Dict, Any, Optional, List

class DeterministicExtractor:
    """Deterministic extractor for numbers, units, quantities, dates/times, and comparison clauses."""

    NUMBER_UNIT_REGEX = re.compile(
        r'(\b\d+(?:\.\d+)?\s*(?:%|percent|mg|g|kg|ml|l|students|pupils|degrees(?:\s+celsius|\s+fahrenheit)?|°c|°f|years|months|weeks|days|hours|percentile)?\b)',
        re.IGNORECASE
    )

    VALUE_REGEX = re.compile(r'(\d+(?:\.\d+)?)')
    PERCENT_REGEX = re.compile(r'(\d+(?:\.\d+)?\s*(?:%|percent))', re.IGNORECASE)
    UNIT_PATTERNS = [
        (re.compile(r'%|percent', re.I), "%"),
        (re.compile(r'mg', re.I), "mg"),
        (re.compile(r'degrees?\s+celsius|°c', re.I), "degrees Celsius"),
        (re.compile(r'degrees?\s+fahrenheit|°f', re.I), "degrees Fahrenheit"),
        (re.compile(r'students?|pupils?', re.I), "students"),
        (re.compile(r'years?', re.I), "years"),
        (re.compile(r'months?', re.I), "months"),
        (re.compile(r'weeks?', re.I), "weeks"),
        (re.compile(r'days?', re.I), "days"),
    ]

    TIME_PATTERNS = re.compile(
        r'\b(daily|weekly|monthly|annually|long-term|short-term|k-3|grade\s+\d+|over\s+\d+\s+years?|in\s+\d{4})\b',
        re.IGNORECASE
    )

    COMPARISON_PATTERNS = re.compile(
        r'\b(improves?\s+by|increases?\s+by|reduces?\s+by|decreases?\s+by|compared\s+to|below\s+\d+|more\s+than|less\s+than|surpasses?)\b',
        re.IGNORECASE
    )

    @classmethod
    def extract_deterministic_fields(cls, text: str) -> Dict[str, Any]:
        result = {
            "value": "Unspecified",
            "unit": "Unspecified",
            "time": "Unspecified",
            "comparison": "Unspecified"
        }

        # 1. Extract Value & Unit
        num_match = cls.NUMBER_UNIT_REGEX.search(text)
        if num_match:
            raw_match = num_match.group(1).strip()
            val_match = cls.VALUE_REGEX.search(raw_match)
            if val_match:
                result["value"] = val_match.group(1)

            # Determine unit
            for pattern, unit_name in cls.UNIT_PATTERNS:
                if pattern.search(raw_match) or pattern.search(text):
                    result["unit"] = unit_name
                    break

        # 2. Extract Time
        time_match = cls.TIME_PATTERNS.search(text)
        if time_match:
            result["time"] = time_match.group(1)

        # 3. Extract Comparison
        comp_match = cls.COMPARISON_PATTERNS.search(text)
        if comp_match:
            result["comparison"] = comp_match.group(1)

        return result
