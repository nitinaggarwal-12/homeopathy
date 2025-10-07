import os
import csv
import json
import re
from typing import List, Dict

def load_repertory(path: str) -> List[Dict]:
    """Load repertory mapping from CSV"""
    out = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            r["weight"] = int(r.get("weight", 1))
            # Keep remedies as string, will be split when needed
            out.append(r)
    return out

def load_materia_medica(mm_dir: str) -> List[Dict]:
    """Load all materia medica files"""
    files = []
    for fn in os.listdir(mm_dir):
        if fn.endswith(".md"):
            with open(os.path.join(mm_dir, fn), "r", encoding="utf-8") as f:
                txt = f.read()
            title = re.sub(r"\.md$", "", fn).replace("_", " ").title()
            files.append({"id": fn, "title": title, "text": txt})
    return files

def save_json(path: str, data):
    """Save JSON data to file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(path: str, default):
    """Load JSON data from file"""
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
