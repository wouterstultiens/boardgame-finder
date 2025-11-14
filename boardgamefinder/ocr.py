# boardgamefinder/ocr.py
from io import BytesIO
from typing import List
import requests
from google.cloud import vision

def extract_text_from_image_urls(image_urls: List[str]) -> List[str]:
    client = vision.ImageAnnotatorClient()
    results = []

    for url in image_urls:
        try:
            # Download the image
            response = requests.get(url, timeout=20)
            response.raise_for_status()

            image = vision.Image(content=response.content)

            # OCR via Google Vision
            resp = client.text_detection(image=image)

            if resp.error.message:
                print(f"Vision error for {url}: {resp.error.message}")
                results.append("")
                continue

            annotations = resp.text_annotations
            text = annotations[0].description if annotations else ""

            results.append(text.strip())

        except Exception as e:
            print(f"Failed to process {url}: {e}")
            results.append("")

    return results
