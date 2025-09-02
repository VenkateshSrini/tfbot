#!/bin/bash

# Terraform Bot API - Startup Script (Linux/macOS)
# Run from the root directory of the project

echo "🚀 Starting Terraform Bot API Server..."
echo "📡 Server will be available at: http://localhost:8000"
echo "📚 API documentation at: http://localhost:8000/docs"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Get the directory where this script is located (should be root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if we're in the right directory (should have tf-bot.py)
if [ ! -f "tf-bot.py" ]; then
    echo "❌ Error: This script must be run from the tfbot root directory"
    echo "   Expected to find tf-bot.py in the current directory"
    exit 1
fi

# Check if api directory exists
if [ ! -d "api" ]; then
    echo "❌ Error: api directory not found"
    echo "   Please ensure you're in the correct project directory"
    exit 1
fi

# Check if uvicorn is installed
python3 -c "import uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing FastAPI and uvicorn..."
    pip3 install fastapi uvicorn[standard]
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        echo "   Please ensure pip3 is installed and try again"
        exit 1
    fi
    echo "✅ Dependencies installed successfully!"
fi

# Check if all required packages are installed
echo "🔍 Checking dependencies..."
python3 -c "
import sys
try:
    import fastapi
    import uvicorn
    from pydantic import BaseModel
    print('✅ All API dependencies are available')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    exit 1
fi

# Start the server from the api directory
echo "🔄 Starting FastAPI server from api directory..."
cd api
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
