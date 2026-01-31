@echo off
echo Starting SPY Trading Bot...
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the app
streamlit run app.py

pause
