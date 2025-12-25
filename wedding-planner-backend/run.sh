#!/bin/bash
# Startup script for Render deployment
cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python src/main.py

