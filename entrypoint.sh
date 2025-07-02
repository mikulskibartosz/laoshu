#!/bin/bash
set -e

# Start FastAPI (CLI web mode) in the background
cd cli
poetry run python __main__.py web --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

cd ..
# Start Next.js frontend in the background
cd frontend
npm start &
NEXT_PID=$!
cd ..

# Wait for both processes
wait $FASTAPI_PID
wait $NEXT_PID