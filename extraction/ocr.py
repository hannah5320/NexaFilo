# extraction/ocr.py

import os
import shutil
import pytesseract
from PIL import Image
import cv2
import numpy as np


def configure_tesseract():
    """
    Configure Tesseract path in a cross-platform way.
    - If Tesseract is in PATH → use it
    - If not found (Windows fallback) → try default install location
    - If still not found → raise helpful error
    """
    tesseract_path = shutil.which("tesseract")

    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    else:
        # Windows fallback
        windows_default = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if os.path.exists(windows_default):
            pytesseract.pytesseract.tesseract_cmd = windows_default
        else:
            raise EnvironmentError(
                "Tesseract is not installed or not in PATH. "
                "Install it and ensure 'tesseract' command works in terminal."
            )


# Configure at import time
configure_tesseract()


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Improve OCR accuracy with preprocessing.
    """
    img = cv2.imread(image_path)

    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove noise
    gray = cv2.medianBlur(gray, 3)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    return thresh


def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from PNG / JPG / JPEG images using Tesseract OCR.
    """
    try:
        processed_img = preprocess_image(image_path)
        pil_img = Image.fromarray(processed_img)

        text = pytesseract.image_to_string(
            pil_img,
            config="--oem 3 --psm 6"
        )

        return text.strip()

    except Exception as e:
        print(f"[OCR Error] {image_path}: {e}")
        return ""
