#!/usr/bin/env python3
"""
LinkedIn Auto Poster - Easy Start Script
এই script দিয়ে একবারেই সব setup করুন এবং application start করুন।
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        sys.exit(1)
    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}")

def check_virtual_environment():
    """Check if running in virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        print("⚠️  Warning: Not running in a virtual environment")
        print("   Consider creating one with: python -m venv .venv")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print("✅ Running in virtual environment")

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def setup_environment():
    """Setup environment configuration"""
    env_file = Path(".env")
    env_template = Path(".env.template")
    
    if not env_file.exists():
        if env_template.exists():
            print("📝 Creating .env file from template...")
            import shutil
            shutil.copy(env_template, env_file)
            print("✅ .env file created")
            print("⚠️  Please edit .env file with your API keys before running!")
            return False
        else:
            print("❌ Neither .env nor .env.template found")
            return False
    else:
        print("✅ .env file exists")
        return True

def check_api_keys():
    """Check if essential API keys are configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_keys = ['OPENAI_API_KEY']
    optional_keys = ['LINKEDIN_ACCESS_TOKEN']
    
    missing_required = []
    missing_optional = []
    
    for key in required_keys:
        if not os.getenv(key) or os.getenv(key) == f"your_{key.lower()}_here":
            missing_required.append(key)
    
    for key in optional_keys:
        if not os.getenv(key) or "your_" in os.getenv(key, ""):
            missing_optional.append(key)
    
    if missing_required:
        print(f"❌ Missing required API keys: {', '.join(missing_required)}")
        return False
    else:
        print("✅ Required API keys configured")
    
    if missing_optional:
        print(f"⚠️  Optional API keys not configured: {', '.join(missing_optional)}")
        print("   The system will work but with limited functionality")
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['logs']
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ Required directories created")

def run_application():
    """Run the main application"""
    print("\n🚀 Starting LinkedIn Auto Poster...")
    try:
        # Import here to avoid import errors during setup
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=os.getenv("DEBUG", "false").lower() == "true",
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

def main():
    """Main setup and start function"""
    print("🔥 LinkedIn Auto Poster Setup & Start")
    print("=" * 50)
    
    # Step 1: Check Python version
    check_python_version()
    
    # Step 2: Check virtual environment
    check_virtual_environment()
    
    # Step 3: Install dependencies
    install_dependencies()
    
    # Step 4: Setup environment
    env_ready = setup_environment()
    
    # Step 5: Create directories
    create_directories()
    
    if not env_ready:
        print("\n⚠️  Setup incomplete!")
        print("Please configure your .env file and run this script again.")
        print("\nRequired steps:")
        print("1. Edit .env file with your API keys")
        print("2. Rerun: python start.py")
        sys.exit(1)
    
    # Step 6: Check API keys
    if not check_api_keys():
        print("\n⚠️  API keys not properly configured!")
        print("Please check your .env file and add the required keys.")
        sys.exit(1)
    
    print("\n✅ All checks passed! Starting application...")
    print("\n📊 Dashboard URL: http://localhost:8000/dashboard")
    print("📋 Health Check: http://localhost:8000/health")
    print("📖 API Docs: http://localhost:8000/docs")
    print("\n Press Ctrl+C to stop\n")
    
    # Step 7: Run the application
    run_application()

if __name__ == "__main__":
    main()