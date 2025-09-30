#!/usr/bin/env bash
set -e
python3 -m venv venv || true
source venv/bin/activate
pip install -r desktop_app/requirements.txt
export $(cat desktop_app/.env.example | xargs)
python desktop_app/app/main.py
