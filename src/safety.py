from typing import Dict, List

RED_FLAGS = [
    "severe chest pain",
    "difficulty breathing",
    "shortness of breath",
    "stroke",
    "paralysis",
    "suicidal",
    "persistent high fever",
    "acute abdomen",
    "severe dyspnea"
]

def has_red_flags(case_json: Dict) -> List[str]:
    """Check case for emergency red flags"""
    text = str(case_json).lower()
    return [rf for rf in RED_FLAGS if rf in text]
