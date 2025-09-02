# Terraform Bot API - Startup Scripts

## Overview

The startup scripts have been moved to the root directory level (same level as `tf-bot.py`) and can now be run from the project root. This makes it easier to manage and ensures proper path resolution.

## Available Startup Scripts

### 1. PowerShell Script (Windows) - `start_api.ps1`
```powershell
.\start_api.ps1
```

### 2. Batch Script (Windows) - `start_api.bat`
```cmd
.\start_api.bat
```

### 3. Shell Script (Linux/macOS) - `start_api.sh`
```bash
chmod +x start_api.sh
./start_api.sh
```

## Features

All scripts include:

- ✅ **Directory Validation**: Ensures you're running from the correct directory
- ✅ **Python Detection**: Verifies Python is installed and accessible
- ✅ **Dependency Check**: Checks for FastAPI, uvicorn, and pydantic
- ✅ **Auto-Installation**: Installs missing dependencies automatically
- ✅ **Error Handling**: Provides clear error messages and troubleshooting
- ✅ **Path Management**: Properly navigates to the API directory for execution
- ✅ **Status Messages**: Colored output showing progress and status

## Script Behavior

1. **Validation Phase**:
   - Checks if running from correct directory (looks for `tf-bot.py`)
   - Verifies `api` directory exists
   - Confirms Python is available

2. **Dependency Phase**:
   - Checks if uvicorn is installed
   - Installs FastAPI and uvicorn if missing
   - Validates all required packages

3. **Startup Phase**:
   - Changes to `api` directory
   - Starts uvicorn server with hot-reload
   - Displays access information

## Requirements

- Python 3.7+ installed and in PATH
- pip package manager
- Internet connection (for dependency installation)

## Troubleshooting

### Common Issues

**"This script must be run from the tfbot root directory"**
- Solution: Navigate to the directory containing `tf-bot.py` before running

**"Python is not installed or not in PATH"**
- Solution: Install Python and ensure it's added to your system PATH

**"Failed to install dependencies"**
- Solution: 
  - Ensure pip is installed: `python -m ensurepip --upgrade`
  - Try manual installation: `pip install fastapi uvicorn[standard]`
  - Check internet connection

**"api directory not found"**
- Solution: Ensure you have the complete project structure with the `api` folder

### Manual Dependency Installation

If automatic installation fails:

```bash
pip install fastapi uvicorn[standard] pydantic
```

### Manual Server Start

If the scripts fail, you can start manually:

```bash
cd api
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Access Points

Once started, the API will be available at:

- **API Endpoint**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Development

For development with auto-reload, the scripts automatically include the `--reload` flag. The server will restart automatically when you make changes to the code.

## Production Deployment

For production deployment, consider:

1. **Docker**: Use the provided `Dockerfile`
2. **Kubernetes**: Use the `k8s/` deployment files
3. **Direct uvicorn**: Run without `--reload` flag for better performance

## Script Locations

```
tfbot/
├── tf-bot.py
├── start_api.ps1      # PowerShell script
├── start_api.bat      # Batch script  
├── start_api.sh       # Shell script
├── api/
│   ├── main.py
│   ├── models.py
│   └── utils.py
└── ...
```

All scripts are now at the root level for easy access and consistent behavior across platforms.
