#!/bin/bash
# Python QR Scanner Setup Script
# Ensures all required dependencies are installed

echo "Installing Python QR Scanner Dependencies..."

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed"
    exit 1
fi

# Install/upgrade required packages
echo "Installing opencv-contrib-python..."
pip install opencv-contrib-python==4.11.0.86

echo "Installing pyzbar..."
pip install pyzbar==0.1.9

echo "Installing Pillow..."
pip install Pillow>=11.1.0

echo "Installing numpy..."
pip install numpy

# Verify installations
echo -e "\nVerifying installations..."

python3 -c "import cv2; print('✓ OpenCV version:', cv2.__version__)" || echo "✗ OpenCV installation failed"
python3 -c "from pyzbar.pyzbar import decode; print('✓ pyzbar installed')" || echo "✗ pyzbar installation failed"
python3 -c "from PIL import Image; print('✓ Pillow installed')" || echo "✗ Pillow installation failed"
python3 -c "import numpy as np; print('✓ NumPy version:', np.__version__)" || echo "✗ NumPy installation failed"

echo -e "\nSetup complete! The Python QR Scanner is ready to use."
echo -e "\nTo use the scanner:"
echo "1. Navigate to the attendance page in the web application"
echo "2. Click 'Start Scanner'"
echo "3. Hold a QR code in front of the camera"
echo "4. The system will automatically detect and mark attendance"
