#!/usr/bin/env python3
"""
Quick Setup Script
==================
Run this to verify your installation is working correctly.
"""

import sys
import subprocess

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("⚠️  Warning: Python 3.9+ recommended")
        return False
    return True

def check_imports():
    """Check if all required packages are installed."""
    packages = [
        ('streamlit', 'streamlit'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('plotly', 'plotly'),
        ('yfinance', 'yfinance'),
        ('ta', 'ta'),
        ('praw', 'praw'),
        ('tweepy', 'tweepy'),
        ('requests', 'requests'),
        ('httpx', 'httpx'),
        ('dotenv', 'python-dotenv'),
        ('pytz', 'pytz'),
    ]
    
    missing = []
    
    for module_name, package_name in packages:
        try:
            __import__(module_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name} - NOT INSTALLED")
            missing.append(package_name)
    
    return missing

def check_ollama():
    """Check if Ollama is running."""
    try:
        import httpx
        response = httpx.get("http://localhost:11434/api/tags", timeout=5.0)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✓ Ollama is running ({len(models)} models available)")
            
            model_names = [m.get('name', '') for m in models]
            if any('llama' in name.lower() for name in model_names):
                print("✓ Llama model found")
            else:
                print("⚠️  No Llama model found. Run: ollama pull llama3.2")
            return True
    except Exception as e:
        print(f"✗ Ollama not running: {e}")
        print("  → Start Ollama or run: ollama serve")
    return False

def check_env_file():
    """Check if .env file exists."""
    from pathlib import Path
    
    env_file = Path(__file__).parent / '.env'
    env_example = Path(__file__).parent / '.env.example'
    
    if env_file.exists():
        print("✓ .env file found")
        return True
    elif env_example.exists():
        print("⚠️  .env file not found")
        print("  → Copy .env.example to .env and add your API keys")
        return False
    else:
        print("✗ No .env or .env.example found")
        return False

def main():
    print("=" * 50)
    print("SPY Trading Bot - Setup Verification")
    print("=" * 50)
    print()
    
    print("📋 Checking Python...")
    check_python_version()
    print()
    
    print("📦 Checking packages...")
    missing = check_imports()
    print()
    
    if missing:
        print("⚠️  Missing packages detected!")
        print("Run this command to install them:")
        print(f"\n  pip install {' '.join(missing)}\n")
    
    print("🤖 Checking Ollama...")
    check_ollama()
    print()
    
    print("📄 Checking configuration...")
    check_env_file()
    print()
    
    print("=" * 50)
    
    if not missing:
        print("✓ Setup looks good!")
        print("\nTo start the bot, run:")
        print("\n  streamlit run app.py\n")
    else:
        print("⚠️  Please install missing packages first")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
