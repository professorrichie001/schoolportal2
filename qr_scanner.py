"""
QR Code Scanner Module using Python
Handles QR code detection from camera frames
"""
import cv2
from pyzbar.pyzbar import decode
import logging
import base64
import io
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

def capture_and_scan_frame():
    """
    Captures a single frame from the camera and attempts to scan QR codes.
    Returns the QR code data if found, None otherwise.
    """
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.error("Failed to open camera")
            return None, None
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            logger.error("Failed to capture frame")
            return None, None
        
        # Decode QR codes from frame
        decoded_objects = decode(frame)
        
        if decoded_objects:
            qr_data = decoded_objects[0].data.decode('utf-8')
            # Also encode the frame as base64 for display
            _, buffer = cv2.imencode('.jpg', frame)
            frame_b64 = base64.b64encode(buffer).decode('utf-8')
            return qr_data, frame_b64
        
        # Return frame even if no QR found
        _, buffer = cv2.imencode('.jpg', frame)
        frame_b64 = base64.b64encode(buffer).decode('utf-8')
        return None, frame_b64
        
    except Exception as e:
        logger.error(f"Error in capture_and_scan_frame: {str(e)}")
        return None, None


def scan_qr_from_base64(image_base64):
    """
    Scans QR code from a base64 encoded image.
    Used for processing images sent from the frontend.
    """
    try:
        # Decode base64 image
        img_data = base64.b64decode(image_base64.split(',')[1] if ',' in image_base64 else image_base64)
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Decode QR codes
        decoded_objects = decode(frame)
        
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
        return None
        
    except Exception as e:
        logger.error(f"Error in scan_qr_from_base64: {str(e)}")
        return None


def extract_admission_number(qr_data):
    """
    Extracts admission number from QR code data.
    Handles multiple QR code formats.
    """
    try:
        # Try to find admission number in various formats
        import re
        
        # Format: "Admission No: ABC/2023/001"
        match = re.search(r'Admission\s*(?:No|Number)?\s*:\s*([^\n]+)', qr_data, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Format: "admission_no=ABC/2023/001"
        match = re.search(r'admission_no=([^\n&]+)', qr_data, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # If no pattern matches, assume entire QR is the admission number
        if '/' in qr_data or qr_data.isnumeric():
            return qr_data.strip()
        
        return None
        
    except Exception as e:
        logger.error(f"Error extracting admission number: {str(e)}")
        return None
