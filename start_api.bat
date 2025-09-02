@echo off
REM Terraform Bot API - Batch Startup Script (Windows)
REM Run from the root directory of the project

echo 🚀 Starting Terraform Bot API Server...
echo.
echo 📡 Server will be available at: http://localhost:8000
echo 📚 API documentation at: http://localhost:8000/docs
echo ⏹️  Press Ctrl+C to stop the server
echo.

REM Change to the directory where this script is located (should be root)
cd /d "%~dp0"

REM Check if we're in the right directory (should have tf-bot.py)
if not exist "tf-bot.py" (
    echo ❌ Error: This script must be run from the tfbot root directory
    echo    Expected to find tf-bot.py in the current directory
    pause
    exit /b 1
)

REM Check if api directory exists
if not exist "api" (
    echo ❌ Error: api directory not found
    echo    Please ensure you're in the correct project directory
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python and ensure it's in your PATH
    pause
    exit /b 1
)

echo ✅ Python is available

REM Check if uvicorn is installed
python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo 📦 Installing FastAPI and uvicorn...
    pip install fastapi uvicorn[standard]
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        echo    Please ensure pip is installed and try again
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed successfully!
)

REM Check if all required packages are installed
echo 🔍 Checking dependencies...
python -c "import sys; import fastapi, uvicorn; from pydantic import BaseModel; print('✅ All API dependencies are available')" 2>nul
if errorlevel 1 (
    echo ❌ Some dependencies are missing
    echo    Please install: pip install fastapi uvicorn[standard] pydantic
    pause
    exit /b 1
)

REM Start the server from the api directory
echo 🔄 Starting FastAPI server from api directory...
cd api
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
