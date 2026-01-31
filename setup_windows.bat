@echo off
echo ==========================================
echo SPY Trading Bot - Quick Start (Windows)
echo ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Could not create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing packages (this may take a few minutes)...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Could not install packages
    pause
    exit /b 1
)

echo [4/4] Checking setup...
python check_setup.py

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To run the trading bot:
echo   1. Make sure Ollama is running (start Ollama app)
echo   2. Run: streamlit run app.py
echo.
echo Or just double-click "run_bot.bat"
echo ==========================================
pause
