#!/usr/bin/env python3
"""
Flatten the sec-api JSON dump into a CSV of Form 4 metadata.
"""

import os
import json
import csv

# Paths
in_path  = "data/raw/form4_api_response.json"
out_dir  = "data/processed"
out_path = os.path.join(out_dir, "form4_api.csv")

# Ensure output dir
os.makedirs(out_dir, exist_ok=True)

# Load JSON
with open(in_path, "r") as f:
    data = json.load(f)

filings = data.get("filings", [])

# Define CSV columns
columns = [
    "accessionNo",
    "ticker",
    "cik",
    "companyName",
    "filedAt",
    "periodOfReport",
    "linkToFilingDetails"
]

# Write CSV
with open(out_path, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()
    for f in filings:
        row = {col: f.get(col, "") for col in columns}
        writer.writerow(row)

print(f"✔ Wrote {len(filings)} rows to {out_path}")
