#!/bin/sh

# export APP_MODULE=${APP_MODULE-src.main:app}
# export HOST=${HOST:-0.0.0.0}
# export PORT=${PORT:-8001}
export PYTHONPATH="$(cd .. && pwd)"
# export IMAGE_DIR="/workspace/data/image"
export IMAGE_DIR="/workspace/data/image"
export DL_URL="http://63.35.31.27:8080"
export FRONT_URL="http://63.35.31.27:3000"
APP_MODULE="main:app"
HOST="0.0.0.0"
PORT="8000"
KEY_PATH="./secure/key.pem"
CERT_PATH="./secure/cert.pem"
# Activate the virtual environment
# source venv/bin/activate

if [ ! -f "$KEY_PATH" ] || [ ! -f "$CERT_PATH" ]
then
    exec openssl req -x509 -newkey rsa:4096 -nodes -out "$CERT_PATH" -keyout "$KEY_PATH" -days 365
fi
# The program is run with the following command:
exec uvicorn --reload  --ssl-keyfile="$KEY_PATH" --ssl-certfile="$CERT_PATH" --host "$HOST" --port "$PORT" "$APP_MODULE" 