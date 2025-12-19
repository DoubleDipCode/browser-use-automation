#!/bin/bash
# Browser-Use Environment Activation Script
# Usage: source ./activate.sh

echo "Activating browser-use environment..."

# Activate virtual environment
source /Users/antonadmin/browser-use-env/bin/activate

# Load API keys
export $(cat /Users/antonadmin/.browser-use.env | xargs)

# Verify
echo "✓ Virtual environment: $(which python)"
echo "✓ Python version: $(python --version)"
echo "✓ OPENAI_API_KEY: ${OPENAI_API_KEY:0:20}..."
echo "✓ GOOGLE_API_KEY: ${GOOGLE_API_KEY:0:15}..."
echo ""
echo "Ready to run browser-use scripts!"
