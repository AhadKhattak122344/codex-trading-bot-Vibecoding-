#!/bin/bash

echo "=========================================="
echo "SPY Trading Bot - Quick Start (Mac/Linux)"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python from https://www.python.org/downloads/"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Could not create virtual environment"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source venv/bin/activate

echo "[3/4] Installing packages (this may take a few minutes)..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Could not install packages"
    exit 1
fi

echo "[4/4] Checking setup..."
python check_setup.py

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run the trading bot:"
echo "  1. Make sure Ollama is running"
echo "  2. Run: source venv/bin/activate && streamlit run app.py"
echo ""
echo "Or just run: ./run_bot.sh"
echo "=========================================="
