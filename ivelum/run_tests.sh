#!/bin/bash
set -e
echo "Hacker News Proxy - Running tests"
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found."
    exit 1
fi
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
pytest -v --cov=app --cov-report=term-missing
