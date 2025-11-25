#!/bin/bash
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
TIMEOUT=${DEFAULT_TIMEOUT:-120}

echo "Iniciando Gunicorn em $HOST:$PORT com timeout de $DEFAULT_TIMEOUT s"
exec gunicorn --timeout $TIMEOUT --bind $HOST:$PORT app:app
