from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from .schema import CaseRecord, SearchQuery
from .repertory import repertorize
from .safety import has_red_flags
from .embeddings import search as mm_search

REPERTORY_PATH = os.getenv("REPERTORY_PATH","../data/repertory_mapping.csv")

app = FastAPI(title="Classical Homeopathy Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CaseIn(BaseModel):
    case: CaseRecord

@app.get("/")
def health():
    return {"status":"ok"}

@app.post("/repertorize")
def api_repertorize(payload: CaseIn):
    case = payload.case.model_dump()
    flags = has_red_flags(case)
    if flags:
        return {"refer_immediately": True, "flags": flags}
    rep = repertorize(case, REPERTORY_PATH)
    return {"refer_immediately": False, "repertory": rep}

@app.post("/mm_search")
def api_mm_search(q: SearchQuery):
    results = mm_search(q.q, k=q.k)
    return {"results": results}
