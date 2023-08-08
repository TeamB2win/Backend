export PYTHONPATH="$(cd .. && pwd)"

export IMAGE_DIR="/workspace/data/image"
export DL_URL="http://172.17.0.1:8080"
export FRONT_URL="http://172.17.0.1:3000"
export DOCS_ENABLE=false
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