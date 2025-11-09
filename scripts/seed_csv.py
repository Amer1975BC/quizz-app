#!/usr/bin/env python3
"""
Import questions from a CSV file and POST them to the admin API.

CSV format (header required):
  text,choices,correct_index

Where 'choices' is pipe-separated, e.g.
  "Wat is 2 + 2?","3|4|5",1

Usage:
  BASE_URL=http://localhost:8000 ./scripts/seed_csv.py path/to/file.csv
"""
import csv
import os
import sys
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")
ADMIN_URL = f"{BASE_URL}/api/admin/questions"

def main(path: str) -> int:
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        required = {"text", "choices", "correct_index"}
        if not required.issubset(reader.fieldnames or []):
            print(f"CSV must include headers: {', '.join(sorted(required))}")
            return 64
        count = 0
        for row in reader:
            text = row["text"].strip()
            choices = [c.strip() for c in row["choices"].split("|") if c.strip()]
            try:
                correct_index = int(row["correct_index"]) if row["correct_index"] != "" else 0
            except ValueError:
                print(f"Invalid correct_index for question: {text}")
                return 65
            payload = {"text": text, "choices": choices, "correct_index": correct_index}
            r = requests.post(ADMIN_URL, json=payload, timeout=10)
            if 200 <= r.status_code < 300:
                count += 1
                print(f"Added: {text}")
            else:
                print(f"FAILED {r.status_code}: {r.text}")
                return 1
    print(f"Done. Added {count} questions.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: seed_csv.py <file.csv>")
        sys.exit(64)
    sys.exit(main(sys.argv[1]))
