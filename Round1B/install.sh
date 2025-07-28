#!/bin/bash

echo "========================================"
echo "PagePilot Installation Script"
echo "Authors: Yugendra N and SuriyaPrakash RM"
echo "========================================"
echo

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

# Check Python version
echo "Python found. Checking version..."
python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if [ $? -ne 0 ]; then
    echo "ERROR: Python 3.8+ is required"
    echo "Current version:"
    python3 --version
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "You may need to install pip3 or use a virtual environment"
    exit 1
fi

# Create directories
echo
echo "Creating directories..."
mkdir -p input output

# Test installation
echo
echo "Testing installation..."
python3 main.py --help > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "WARNING: Installation test failed"
    echo "You may need to check your setup"
else
    echo "SUCCESS: PagePilot installed successfully!"
fi

echo
echo "========================================"
echo "Installation Complete!"
echo
echo "To get started:"
echo "1. Place your PDF files in the 'input' folder"
echo "2. Configure 'input/analysis_request.json'"
echo "3. Run: python3 main.py"
echo "========================================"
