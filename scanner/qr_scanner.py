import cv2
import numpy as np
from PIL import Image
import os

try:
    from pyzbar.pyzbar import decode as pyzbar_decode
except (ImportError, OSError):
    pyzbar_decode = None

# Import URL phishing detector
from scanner.url_scanner import scan_url


def preprocess_image(image_path):
    """
    Improve QR detection for screenshots and camera photos.
    """

    img = cv2.imread(image_path)

    if img is None:
        return None

    # Resize large images
    height, width = img.shape[:2]
    if width > 1200:
        scale = 1200 / width
        img = cv2.resize(img, None, fx=scale, fy=scale)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.equalizeHist(gray)

    # Remove noise
    blur = cv2.GaussianBlur(gray, (3,3), 0)

    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return img, gray, thresh


def decode_qr(image_path):
    """
    Try multiple methods to decode QR.
    """

    processed = preprocess_image(image_path)

    if processed is None:
        return None

    original, gray, thresh = processed

    if pyzbar_decode is not None:
        # ---------- Method 1 : Pyzbar Original ----------
        decoded = pyzbar_decode(original)
        if decoded:
            return decoded[0].data.decode("utf-8")

        # ---------- Method 2 : Grayscale ----------
        decoded = pyzbar_decode(gray)
        if decoded:
            return decoded[0].data.decode("utf-8")

        # ---------- Method 3 : Threshold Image ----------
        decoded = pyzbar_decode(thresh)
        if decoded:
            return decoded[0].data.decode("utf-8")

    # ---------- Method 4 : OpenCV QRCodeDetector ----------
    detector = cv2.QRCodeDetector()

    data, bbox, _ = detector.detectAndDecode(original)
    if data:
        return data

    data, bbox, _ = detector.detectAndDecode(gray)
    if data:
        return data

    data, bbox, _ = detector.detectAndDecode(thresh)
    if data:
        return data

    return None


def analyze_qr(image_path):
    """
    Analyze uploaded QR code.
    """

    qr_content = decode_qr(image_path)

    if qr_content is None:
        return {
            "prediction": "Unreadable QR Code",
            "confidence": 0,
            "decoded_url": "",
            "reasons": [
                "QR code could not be detected.",
                "Image may be damaged or not contain a QR code."
            ]
        }

    # If QR contains URL -> AI URL Scanner
    if qr_content.startswith("http://") or qr_content.startswith("https://"):
        result = scan_url(qr_content)

        return {
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "decoded_url": qr_content,
            "reasons": result["reasons"]
        }

    # WhatsApp QR
    if "whatsapp" in qr_content.lower():
        return {
            "prediction": "Safe",
            "confidence": 98,
            "decoded_url": qr_content,
            "reasons": [
                "WhatsApp QR code detected.",
                "No phishing URL found."
            ]
        }

    # UPI QR
    if qr_content.startswith("upi://"):
        return {
            "prediction": "Safe",
            "confidence": 96,
            "decoded_url": qr_content,
            "reasons": [
                "UPI payment QR detected.",
                "Verify receiver name before payment."
            ]
        }

    # Other QR Content
    return {
        "prediction": "Safe",
        "confidence": 90,
        "decoded_url": qr_content,
        "reasons": [
            "QR code decoded successfully.",
            "No malicious URL detected."
        ]
    }