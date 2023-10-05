import cv2
from dotenv import load_dotenv
import os
from pytesseract import pytesseract
# Path: tagDetector.py

def tagDetect(TessPath):
    camera = cv2.VideoCapture(0)
    tesseractPath = TessPath

    pytesseract.tesseract_cmd = tesseractPath

    while True:
        ret, frame = camera.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        text = pytesseract.image_to_string(gray)

        if any(char.isdigit() for char in text):
            return text

    camera.release()
    cv2.destroyAllWindows()