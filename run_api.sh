#!/bin/bash
# Start the Browser-Use API Server

set -e

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
source /Users/antonadmin/browser-use-env/bin/activate

# Load environment variables
export $(cat /Users/antonadmin/.browser-use.env | grep -v '^#' | xargs)

# Save PID
echo $$ > /tmp/browser-use-api.pid

echo "Starting Browser-Use API Server..."
echo "PID: $$"
echo "Logs: logs/api.log"
echo "Press Ctrl+C to stop"

# Start server
uvicorn api.server:app \
  --host "${API_HOST:-0.0.0.0}" \
  --port "${API_PORT:-8000}" \
  --log-config logging.yaml

# Cleanup PID file on exit
rm -f /tmp/browser-use-api.pid
