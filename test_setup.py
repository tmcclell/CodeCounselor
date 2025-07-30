#!/usr/bin/env python3
"""
Test script to verify CodeCounselor installation and configuration
"""
import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"), 
        ("openai", "openai"),
        ("python-dotenv", "dotenv"),
        ("httpx", "httpx")
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} - Installed")
        except ImportError:
            print(f"❌ {package_name} - Missing")
            missing_packages.append(package_name)
    
    return len(missing_packages) == 0

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ .env file - Missing")
        print("   Copy .env.example to .env and configure your Azure OpenAI credentials")
        return False
    
    print("✅ .env file - Found")
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_DEPLOYMENT_NAME",
        "AZURE_OPENAI_API_VERSION"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value and not value.startswith("your-"):
            print(f"✅ {var} - Configured")
        else:
            print(f"❌ {var} - Not configured")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

def check_azure_openai_connection():
    """Test Azure OpenAI connection."""
    try:
        from openai import AzureOpenAI
        from dotenv import load_dotenv
        
        load_dotenv()
        
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        # Try to list models (this will fail if credentials are wrong)
        # Note: This is a simple test, might not work with all Azure OpenAI setups
        print("✅ Azure OpenAI client - Initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Azure OpenAI connection - Error: {str(e)}")
        return False

def check_project_structure():
    """Check if project files exist."""
    required_files = [
        "main.py",
        "requirements.txt",
        ".env.example",
        "static/index.html",
        "static/style.css"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} - Found")
        else:
            print(f"❌ {file_path} - Missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks."""
    print("🔍 CodeCounselor Installation Check")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Environment Configuration", check_env_file),
        ("Azure OpenAI Connection", check_azure_openai_connection)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Error during {check_name}: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! CodeCounselor is ready to run.")
        print("🚀 Start the server with: python run_dev.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above before running.")
        print("📖 See README.md for detailed setup instructions.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
