import cv2
from pyzbar.pyzbar import decode
import io
import logging


def scan_qr_with_camera():
    """Scans a QR code using the device camera and ensures it reopens properly."""
    while True:  # Ensure the camera can restart each time
        cap = cv2.VideoCapture(0)  # Open camera every time function is called
        print("Scanning for QR code... Press 'q' to exit.")
        
        while cap.isOpened():  # Make sure the camera is active
            ret, frame = cap.read()
            if not ret:
                break

            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_data = obj.data.decode("utf-8")
                cap.release()  # Release camera
                cv2.destroyAllWindows()  # Close the scanning window
                False
                return qr_data  # Return detected QR code
            
            cv2.imshow("QR Code Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()  # Ensure camera is released if loop exits
        cv2.destroyAllWindows()
        print("Restarting scanner...")

choice = input("Wanna scan with the camera")

if choice == "yes":
    print(scan_qr_with_camera())

