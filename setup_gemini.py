#!/usr/bin/env python3
"""
Setup script for Gemini API configuration
"""

import os
from pathlib import Path

def setup_env_file():
    """Create .env file from template"""
    env_example_path = Path(".env.example")
    env_path = Path(".env")
    
    if env_path.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example_path.exists():
        print("❌ .env.example file not found")
        return False
    
    # Copy example to .env
    with open(env_example_path, 'r') as f:
        content = f.read()
    
    with open(env_path, 'w') as f:
        f.write(content)
    
    print("✅ Created .env file from template")
    print("⚠️  Please edit .env file and add your Gemini API key")
    return True

def install_dependencies():
    """Install required packages"""
    import subprocess
    try:
        print("📦 Installing required packages...")
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def main():
    print("🚀 Setting up Gemini API for Image Caption Generator")
    print("=" * 50)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        return
    
    # Step 2: Setup environment file
    setup_env_file()
    
    print("\n📋 Next Steps:")
    print("1. Get your Gemini API key from: https://aistudio.google.com/app/apikey")
    print("2. Edit the .env file and replace 'your_gemini_api_key_here' with your actual API key")
    print("3. Run the application: python app_gemini.py")
    print("4. Open http://localhost:5000 in your browser")
    
    print("\n💡 Note: Gemini API offers free tier with generous limits for testing")

if __name__ == "__main__":
    main()
