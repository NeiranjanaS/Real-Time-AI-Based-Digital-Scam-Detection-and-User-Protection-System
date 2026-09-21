import cv2

try:
    import zxingcpp
except ImportError:
    zxingcpp = None


def decode_qr(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None

    if zxingcpp is not None:
        for barcode in zxingcpp.read_barcodes(image):
            if barcode.text:
                return barcode.text

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variants = [image, gray]

    # WhatsApp images are often compressed or scaled down, so give the
    # detector higher-contrast and larger inputs as well as the original.
    if max(gray.shape) < 1600:
        variants.append(cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC))

    variants.extend([
        cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 5
        ),
    ])

    detector = cv2.QRCodeDetector()
    for variant in variants:
        decoded_text, _, _ = detector.detectAndDecode(variant)
        if decoded_text:
            return decoded_text

        multi_result = detector.detectAndDecodeMulti(variant)
        if multi_result[0]:
            for decoded_text in multi_result[1]:
                if decoded_text:
                    return decoded_text

    return None