export PYTHONPATH="$(cd .. && pwd)"

export IMAGE_DIR="/workspace/data/image"
export DL_URL="http://172.17.0.1:8080"
export FRONT_URL="http://172.17.0.1:3000"
export DOCS_ENABLE=false
APP_MODULE="main:app"
HOST="0.0.0.0"
PORT="8000"

# Activate the virtual environment
# source venv/bin/activate

# The program is run with the following command:
exec uvicorn --reload --host "$HOST" --port "$PORT" "$APP_MODULE"