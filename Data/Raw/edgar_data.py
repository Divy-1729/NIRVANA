#!/usr/bin/env python3
"""
Fetch Form 4 filings via sec-api and store the full response to JSON.
"""

import os
import json
from sec_api import QueryApi

# ── CONFIG ──
API_KEY    = "4302d0c2f3039796d5d2dc47319ad007787eb9ed27d568c054dfef0e064257a1"
TICKER     = "AAPL"
START_DATE = "2019-01-01"
END_DATE   = "2023-12-31"
PAGE_SIZE  = 50

# ── SETUP ──
out_dir = "data/raw"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "form4_api_response.json")

query_api = QueryApi(api_key=API_KEY)
all_filings = []
offset = 0

# Build the Lucene query
search_query = (
    f'ticker:{TICKER} AND formType:"4" '
    f'AND filedAt:[{START_DATE} TO {END_DATE}]'
)

while True:
    params = {
        "query": search_query,
        "from": str(offset),
        "size": str(PAGE_SIZE),
        "sort": [{"filedAt": {"order": "desc"}}]
    }
    response = query_api.get_filings(params)
    filings = response.get("filings", [])
    if not filings:
        break

    all_filings.extend(filings)
    print(f"⚡ Retrieved {len(filings)} filings (offset {offset})")
    offset += PAGE_SIZE

# ── WRITE TO JSON ──
with open(out_path, "w") as f:
    json.dump({"filings": all_filings}, f, indent=2)

print(f"✅ Wrote {len(all_filings)} filings to {out_path}")
