#!/usr/bin/env python3
"""
Streamlit runner for CodeCounselor frontend
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run the CodeCounselor Streamlit frontend."""
    # Change to the script's directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🚀 Starting CodeCounselor Streamlit frontend...")
    print("📍 Streamlit app will be available at: http://localhost:8501")
    print("🔗 Make sure FastAPI backend is running at: http://localhost:8000")
    print()
    print("Press Ctrl+C to stop the app")
    print("-" * 50)
    
    try:
        # Run streamlit
        python_exe = sys.executable
        cmd = [
            python_exe, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 CodeCounselor Streamlit frontend stopped. Thanks for using our therapy services!")
        return 0
    except Exception as e:
        print(f"❌ Error starting Streamlit app: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())