#!/bin/bash

cd /site/movie_suggestor

echo "Installing dependencies..."
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt

echo "Starting Flask API..."
cd "$(dirname "$0")/bin/api"
python app.py &

FLASK_PID=$!

sleep 2

echo "Starting React app..."
cd "$(dirname "$0")/bin"
npm run dev &

REACT_PID=$!

cleanup() {
    echo "Shutting down services..."
    kill $FLASK_PID
    kill $REACT_PID
    exit 0
}

trap cleanup SIGINT SIGTERM

wait