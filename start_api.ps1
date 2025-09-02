# Terraform Bot API - PowerShell Startup Script (Windows)
# Run from the root directory of the project

Write-Host "🚀 Starting Terraform Bot API Server..." -ForegroundColor Green
Write-Host "📡 Server will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API documentation at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Get the directory where this script is located (should be root)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

# Check if we're in the right directory (should have tf-bot.py)
if (-not (Test-Path "tf-bot.py")) {
    Write-Host "❌ Error: This script must be run from the tfbot root directory" -ForegroundColor Red
    Write-Host "   Expected to find tf-bot.py in the current directory" -ForegroundColor Red
    exit 1
}

# Check if api directory exists
if (-not (Test-Path "api" -PathType Container)) {
    Write-Host "❌ Error: api directory not found" -ForegroundColor Red
    Write-Host "   Please ensure you're in the correct project directory" -ForegroundColor Red
    exit 1
}

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "   Please install Python and ensure it's in your PATH" -ForegroundColor Red
    exit 1
}

# Check if uvicorn is installed
try {
    python -c "import uvicorn" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "📦 Installing FastAPI and uvicorn..." -ForegroundColor Yellow
        pip install fastapi uvicorn[standard]
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
            Write-Host "   Please ensure pip is installed and try again" -ForegroundColor Red
            exit 1
        }
        Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error checking uvicorn: $_" -ForegroundColor Red
    exit 1
}

# Check if all required packages are installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow
try {
    python -c @"
import sys
try:
    import fastapi
    import uvicorn
    from pydantic import BaseModel
    print('✅ All API dependencies are available')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    sys.exit(1)
"@
    
    if ($LASTEXITCODE -ne 0) {
        exit 1
    }
} catch {
    Write-Host "❌ Error checking dependencies: $_" -ForegroundColor Red
    exit 1
}

# Start the server from the api directory
Write-Host "🔄 Starting FastAPI server from api directory..." -ForegroundColor Green
try {
    Set-Location "api"
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
} catch {
    Write-Host "❌ Failed to start server: $_" -ForegroundColor Red
    exit 1
}
