"""
Startup script for Terraform Bot API
Run this script to start the FastAPI server
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing FastAPI requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn[standard]"])
        print("✅ FastAPI requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def start_api_server():
    """Start the FastAPI server"""
    print("🚀 Starting Terraform Bot API server...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API documentation will be available at: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    
    try:
        import uvicorn
        # Change to the api directory
        api_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(api_dir)
        
        # Start the server
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except ImportError:
        print("❌ uvicorn not installed. Installing now...")
        if install_requirements():
            import uvicorn
            uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
        else:
            print("❌ Failed to install requirements. Please install manually:")
            print("   pip install fastapi uvicorn[standard]")
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_api_server()
