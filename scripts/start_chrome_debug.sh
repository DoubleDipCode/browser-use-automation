#!/bin/bash
# Start Chrome with Remote Debugging
# This allows browser-use to connect to your real Chrome profile

echo "🔴 Stopping any running Chrome instances..."
pkill -9 "Google Chrome" 2>/dev/null
sleep 2

echo "🚀 Starting Chrome with remote debugging on port 9222..."
# Note: Chrome requires a non-default data directory for remote debugging
# Using a dedicated directory for browser-use automation
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.config/browseruse/chrome-debug" \
  --no-first-run \
  > /tmp/chrome-debug.log 2>&1 &

sleep 3

# Test connection
echo "🔍 Testing CDP connection..."
if curl -s http://localhost:9222/json/version > /dev/null 2>&1; then
    echo "✅ Chrome debugging port is ready on http://localhost:9222"
    echo "✅ You can now run: python scripts/linkedin_navigate.py"
    echo ""
    curl -s http://localhost:9222/json/version | python3 -m json.tool
else
    echo "❌ Failed to start Chrome with debugging"
    echo "Check /tmp/chrome-debug.log for errors"
    exit 1
fi
