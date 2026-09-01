import cv2

def scan_qr(image_path):
    image = cv2.imread(image_path)

    detector = cv2.QRCodeDetector()

    data, bbox, _ = detector.detectAndDecode(image)

    if bbox is None or data == "":
        return None

    return data