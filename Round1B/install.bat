@echo off
echo ========================================
echo PagePilot Installation Script
echo Authors: Yugendra N and SuriyaPrakash RM
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Checking version...
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.8+ is required
    echo Current version:
    python --version
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Creating directories...
if not exist "input" mkdir input
if not exist "output" mkdir output

echo.
echo Testing installation...
python main.py --help >nul 2>&1
if errorlevel 1 (
    echo WARNING: Installation test failed
    echo You may need to check your setup
) else (
    echo SUCCESS: PagePilot installed successfully!
)

echo.
echo ========================================
echo Installation Complete!
echo.
echo To get started:
echo 1. Place your PDF files in the 'input' folder
echo 2. Configure 'input/analysis_request.json'
echo 3. Run: python main.py
echo ========================================
pause
