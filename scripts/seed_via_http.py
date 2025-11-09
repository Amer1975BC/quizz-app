#!/usr/bin/env python3
"""
Seed questions via the admin HTTP API.

Assumptions:
- Admin endpoints are available without auth at /api/admin/questions
- Payload format: {"text": str, "choices": [str, ...], "correct_index": int}

Usage:
  BASE_URL=http://localhost:8000 ./scripts/seed_via_http.py data/questions.sample.json

If BASE_URL is not provided, defaults to http://localhost:8000.
Run this inside the quiz-app container to reach the FastAPI service directly.
"""
import json
import os
import sys
import time

import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")
ADMIN_URL = f"{BASE_URL}/api/admin/questions"

def main(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print("Input must be a JSON array of questions")
        return 2

    ok = 0
    for idx, q in enumerate(data, 1):
        payload = {
            "text": q.get("text"),
            "choices": q.get("choices", []),
            "correct_index": q.get("correct_index", 0),
        }
        r = requests.post(ADMIN_URL, json=payload, timeout=10)
        if r.status_code >= 200 and r.status_code < 300:
            ok += 1
            print(f"[{idx}/{len(data)}] added: {payload['text']}")
        else:
            print(f"[{idx}/{len(data)}] FAILED {r.status_code}: {r.text}")
        time.sleep(0.05)

    print(f"Done. Added {ok}/{len(data)} questions.")
    return 0 if ok == len(data) else 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: seed_via_http.py <questions.json>")
        sys.exit(64)
    sys.exit(main(sys.argv[1]))
