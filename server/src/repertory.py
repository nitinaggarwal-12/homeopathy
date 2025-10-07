import os
from typing import Dict
from .utils import load_repertory

def repertorize(case_json: Dict, repertory_path: str) -> Dict:
    repertory = load_repertory(repertory_path)
    texts = []
    fields = ["presenting_complaint","etiology","thermal"]
    for k in fields:
        if case_json.get(k):
            texts.append(str(case_json[k]).lower())

    for key in ["mental_emotional","generals","cravings","aversions","sleep","dreams","past_history","family_history","lifestyle"]:
        for v in case_json.get(key, []):
            texts.append(str(v).lower())

    for p in case_json.get("particulars", []):
        texts.append(str(p.get("description","")).lower())
        texts += [s.lower() for s in p.get("modalities_better",[]) + p.get("modalities_worse",[]) + p.get("concomitants",[])]

    full_text = " ".join(texts)
    hits = []
    remedy_scores = {}
    for row in repertory:
        kws = [k.strip().lower() for k in row["keywords"].split(",")]
        matched = [k for k in kws if k and k in full_text]
        if matched:
            hits.append(dict(
                rubric=row["rubric"],
                weight=row["weight"],
                remedies=row["candidate_remedies"],
                matched_keywords=matched
            ))
            for rem in row["candidate_remedies"]:
                remedy_scores[rem] = remedy_scores.get(rem, 0) + row["weight"]

    ranked = sorted(remedy_scores.items(), key=lambda x: x[1], reverse=True)
    candidates = [{"name": r, "score": float(s), "reasons": []} for r, s in ranked[:10]]
    return {"hits": hits, "candidates": candidates}
