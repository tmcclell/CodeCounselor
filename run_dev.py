#!/usr/bin/env python3
"""
Development runner for CodeCounselor
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run the CodeCounselor application in development mode."""
    # Change to the script's directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("⚠️  No .env file found!")
        print("Please copy .env.example to .env and configure your Azure OpenAI credentials:")
        print("  cp .env.example .env")
        print()
        print("Required environment variables:")
        print("  - AZURE_OPENAI_ENDPOINT")
        print("  - AZURE_OPENAI_API_KEY") 
        print("  - AZURE_OPENAI_DEPLOYMENT_NAME")
        print("  - AZURE_OPENAI_API_VERSION")
        return 1
    
    print("🚀 Starting CodeCounselor development server...")
    print("📍 Application will be available at: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("🌐 Frontend: http://localhost:8000/static/index.html")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run uvicorn with the correct python executable
        python_exe = sys.executable
        cmd = [
            python_exe, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--log-level", "info"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 CodeCounselor server stopped. Thanks for using our therapy services!")
        return 0
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
