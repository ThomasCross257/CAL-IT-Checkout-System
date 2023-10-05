import cv2
from pytesseract import pytesseract
# Path: tagDetector.py

def tagDetect(TessPath):
    camera = cv2.VideoCapture(0)
    tesseractPath = TessPath

    pytesseract.tesseract_cmd = tesseractPath

    while True:
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        if any(char.isdigit() for char in text):
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')