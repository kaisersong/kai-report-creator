#!/usr/bin/env bash
# kai-report-creator — run automated tests
#
# Usage:
#   ./run_tests.sh           # all tests (unit + Playwright)
#   ./run_tests.sh --fast    # unit tests only (no browser, ~1 s)
#
# First-time setup:
#   pip install -r requirements-test.txt
#   playwright install chromium

set -euo pipefail
cd "$(dirname "$0")"

echo "══════════════════════════════════════════"
echo "  kai-report-creator · automated tests"
echo "══════════════════════════════════════════"

if [ "${1-}" = "--fast" ]; then
  echo "Mode: unit tests only (--fast)"
  python -m pytest tests/test_export_config.py "$@"
else
  echo "Mode: full suite (unit + Playwright)"
  python -m pytest tests/ "$@"
fi
