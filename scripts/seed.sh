#!/usr/bin/env bash
set -euo pipefail

# Helper to run seeding inside the running container via admin HTTP API.
# Usage:
#   ./scripts/seed.sh data/questions.sample.json

JSON_PATH=${1:-data/questions.sample.json}

# If running on the host with docker compose, execute inside the quiz-app container.
if grep -q "services:" docker-compose.yml 2>/dev/null || [ -f docker-compose.yaml ]; then
  echo "Running seeder in container..."
  docker compose exec -T -w /app quiz-app env BASE_URL=http://localhost:8000 python scripts/seed_via_http.py "$JSON_PATH"
else
  echo "Running seeder locally against BASE_URL=${BASE_URL:-http://localhost:8000}"
  env BASE_URL="${BASE_URL:-http://localhost:8000}" python scripts/seed_via_http.py "$JSON_PATH"
fi
