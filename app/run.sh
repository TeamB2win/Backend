#!/bin/sh

# export APP_MODULE=${APP_MODULE-src.main:app}
# export HOST=${HOST:-0.0.0.0}
# export PORT=${PORT:-8001}
export PYTHONPATH="$(cd .. && pwd)"
APP_MODULE="main:app"
HOST="0.0.0.0"
PORT="8000"

# Activate the virtual environment
# source venv/bin/activate

# The program is run with the following command:
exec uvicorn --reload --host "$HOST" --port "$PORT" "$APP_MODULE"