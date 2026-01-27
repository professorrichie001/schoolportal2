# Python-Based QR Code Scanner Implementation

## Overview
Successfully migrated QR code scanning from JavaScript (jsQR library) to Python-based server-side scanning using OpenCV and pyzbar.

## Key Changes Made

### 1. New Python Module: `qr_scanner.py`
**Location:** `/home/mesh/schoolportal/qr_scanner.py`

**Functions:**
- `capture_and_scan_frame()` - Captures a frame from camera and detects QR codes
- `scan_qr_from_base64()` - Scans QR code from base64 encoded image
- `extract_admission_number()` - Extracts admission number from QR code data in multiple formats

**Features:**
- Uses OpenCV (cv2) for camera access
- Uses pyzbar for QR code detection
- Returns both QR data and base64 encoded frame for display
- Handles multiple admission number formats

### 2. Updated Flask Backend: `app2.py`
**New Routes Added:**

#### `/scan_qr_python` (GET)
- Server-side QR code scanning
- Captures frame from camera
- Returns detected QR code data and camera frame
- Response includes:
  - `success`: Operation status
  - `qr_detected`: Whether QR code was found
  - `admission_no`: Extracted admission number
  - `frame`: Base64 encoded camera frame

#### `/scan_qr_from_image` (POST)
- Scans QR code from image uploaded from client
- Accepts base64 encoded image
- Returns admission number if QR detected

### 3. Updated Frontend: `attendance.html`
**Key Improvements:**

#### Removed:
- JavaScript jsQR library dependency
- Client-side video stream handling
- Browser-based camera access limitations

#### Added:
- Python QR scanner integration
- Server-side camera feed display (via base64 frames)
- Polling-based scanning (every 500ms)
- Real-time scanning status display
- Better error handling and user feedback

**New JavaScript Functions:**
- `startPythonScanner()` - Initiates server-side scanning loop
- `stopPythonScanner()` - Stops scanning
- `performPythonQRScan()` - Sends scan request to server
- `updateScanningStatus()` - Updates UI with scanning status

## How It Works

1. **User clicks "Start Scanner"**
   - JavaScript initiates polling to `/scan_qr_python`
   - Every 500ms, a scan request is sent to the server

2. **Server-side Processing**
   - Python captures a frame from the camera
   - pyzbar library analyzes the frame for QR codes
   - If QR detected, admission number is extracted
   - Frame is encoded as base64 and returned

3. **Frontend Display**
   - Camera frame is displayed as image (updated every 500ms)
   - If QR code detected, student is marked present
   - Scanner automatically restarts after 2 seconds

4. **Manual Fallback**
   - Users can switch to manual entry mode
   - Type admission number directly
   - Press Enter or click "Mark Present"

## Advantages Over JavaScript Scanning

1. **Server-side Processing**
   - More reliable QR code detection
   - Uses OpenCV and pyzbar (battle-tested libraries)
   - No browser compatibility issues

2. **Better Visibility**
   - Actual camera feed displayed to user
   - Clear feedback on scanning status
   - No reliance on JavaScript video API

3. **Camera Access**
   - Python/server has direct access to camera
   - No browser permission dialogs
   - More flexible camera handling

4. **Robust Detection**
   - pyzbar is highly reliable for QR code detection
   - Handles various QR code orientations
   - Better performance than JavaScript alternatives

## Dependencies

Already installed in `requirements.txt`:
- `opencv-contrib-python==4.11.0.86` - Camera access and frame processing
- `pyzbar==0.1.9` - QR code detection
- `Pillow>=11.1.0` - Image processing
- `numpy` - Numerical operations (via opencv)

## Testing

To test the new scanner:

1. Navigate to the attendance page
2. Click "Start Scanner"
3. Hold a student QR code in front of the camera
4. The system will detect and mark the student present automatically
5. Scanner resumes for next student

## Troubleshooting

**No camera feed visible:**
- Check camera permissions on the system
- Verify camera is accessible: `ls -la /dev/video*`
- Check server logs for OpenCV errors

**QR codes not detected:**
- Ensure good lighting
- Keep QR code within frame center
- Check QR code quality

**Module import errors:**
- Install dependencies: `pip install -r requirements.txt`
- Verify pyzbar: `python -c "from pyzbar.pyzbar import decode; print('OK')"`
