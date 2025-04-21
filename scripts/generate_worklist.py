# /scripts/generate_worklist.py
"""
Read regulators_raw, enrich it with access metadata, and
write two outputs:
  1. MongoDB collection 'regulators_worklist'
  2. JSON file worklist_<YYYYMMDD>.json   (for manual inspection)
"""

import re, json, pathlib, datetime as dt
from pymongo import MongoClient
from bson import json_util

MONGO_URI = "mongodb://localhost:27017"
DB_NAME    = "roaming_tracker"
RAW_COLL   = "regulators_raw"
WL_COLL    = "regulators_worklist"
JSON_OUT   = pathlib.Path("data/worklist_" + dt.datetime.utcnow().strftime("%Y%m%d") + ".json")

# optional: domains we KNOW are JS‑heavy
JS_HEAVY_SITES = {"regulation.gov.cn", "gov.uk", "europa.eu"}

def split_methods(cell:str):
    if not cell or not isinstance(cell, str):
        return []
    items = re.split(r"[;,/]", cell)
    return [item.strip().upper() for item in items if item.strip()]

def derive_primary(methods):
    for m in ("API", "HTML", "PDF"):
        if m in methods:
            return m
    return methods[0] if methods else "UNKNOWN"

def detect_headless(row, methods, primary):
    if primary != "HTML":
        return False
    if "JAVASCRIPT" in (row.get("access_method","").upper()):
        return True
    domain = row.get("website","").split("/")[-1]
    return domain in JS_HEAVY_SITES

def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    raw = list(db[RAW_COLL].find({}))
    if not raw:
        raise SystemExit("Raw collection empty – run load_regulators_excel.py first.")

    enriched = []
    ts = dt.datetime.utcnow()
    for row in raw:
        methods = split_methods(row.get("access_method", ""))
        primary = derive_primary(methods)
        headless = detect_headless(row, methods, primary)

        payload = {
            **row,                       # keep original fields
            "access_methods": methods,
            "primary_method": primary,
            "needs_headless": headless,
            "language": row.get("language", "Unknown"),
            "worklist_ts": ts,
        }
        # Remove Mongo _id if we upsert into a new collection
        payload.pop("_id", None)
        enriched.append(payload)

    wl = db[WL_COLL]
    wl.delete_many({})
    wl.insert_many(enriched)
    print(f"Inserted {len(enriched)} docs → {DB_NAME}.{WL_COLL}")

    # JSON pretty‑dump for manual review
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    with JSON_OUT.open("w", encoding="utf‑8") as f:
        json.dump(enriched, f, default=json_util.default, indent=2)
    print(f"Wrote {JSON_OUT}")

if __name__ == "__main__":
    main()
