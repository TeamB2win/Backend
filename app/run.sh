#!/bin/sh

# export APP_MODULE=${APP_MODULE-src.main:app}
# export HOST=${HOST:-0.0.0.0}
# export PORT=${PORT:-8001}
export PYTHONPATH="$(cd .. && pwd)"
# export IMAGE_DIR="/workspace/data/image"
export IMAGE_DIR="/Users/magenta/Downloads"
export DL_URL="http://63.35.31.27:8080"
export FRONT_URL="http://63.35.31.27:"
APP_MODULE="main:app"
HOST="0.0.0.0"
PORT="8000"

# Activate the virtual environment
# source venv/bin/activate

# The program is run with the following command:
exec uvicorn --reload --host "$HOST" --port "$PORT" "$APP_MODULE"