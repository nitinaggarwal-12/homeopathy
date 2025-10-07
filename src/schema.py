from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any

class Symptom(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    section: str
    description: str
    modalities_better: List[str] = []
    modalities_worse: List[str] = []
    concomitants: List[str] = []

class CaseRecord(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    presenting_complaint: str
    onset: Optional[str] = None
    duration: Optional[str] = None
    course: Optional[str] = None
    etiology: Optional[str] = None
    mental_emotional: List[str] = []
    generals: List[str] = []
    particulars: List[Symptom] = []
    cravings: List[str] = []
    aversions: List[str] = []
    sleep: List[str] = []
    dreams: List[str] = []
    thermal: Optional[str] = None
    past_history: List[str] = []
    family_history: List[str] = []
    lifestyle: List[str] = []
    red_flags: List[str] = []

class SearchQuery(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    q: str
    k: int = 5
