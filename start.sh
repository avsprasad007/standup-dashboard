#!/usr/bin/env zsh
set -e
cd "$(dirname "$0")"
echo "Starting Team Emails Gmail Ingestor UI at http://127.0.0.1:8765 ..."
./.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8765 --reload
