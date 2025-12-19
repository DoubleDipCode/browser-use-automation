#!/bin/bash
# Stop the Browser-Use API Server

PID_FILE="/tmp/browser-use-api.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    echo "Stopping Browser-Use API Server (PID: $PID)..."

    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        echo "Server stopped"
    else
        echo "Process $PID not running"
    fi

    rm -f "$PID_FILE"
else
    echo "PID file not found. Server may not be running."
    echo "Trying to find and kill uvicorn processes..."

    pkill -f "uvicorn api.server:app" && echo "Server processes killed" || echo "No running server found"
fi
