# src/boardgamefinder/adapters/ocr_client.py
from typing import List
import requests
from google.cloud import vision

class OcrClient:
    """A client for performing OCR using Google Cloud Vision API."""
    def __init__(self):
        self._client = vision.ImageAnnotatorClient()
        print("Google Vision OcrClient initialized.")

    def extract_text_from_urls(self, image_urls: List[str]) -> List[str]:
        """Extracts text from a list of image URLs."""
        results = []
        if not image_urls:
            return results

        print(f"Performing OCR on {len(image_urls)} images...")
        for url in image_urls:
            try:
                response = requests.get(url, timeout=20)
                response.raise_for_status()

                image = vision.Image(content=response.content)
                resp = self._client.text_detection(image=image)

                if resp.error.message:
                    print(f"Vision API error for {url}: {resp.error.message}")
                    results.append("")
                    continue

                text = resp.text_annotations[0].description if resp.text_annotations else ""
                results.append(text.strip())
            except Exception as e:
                print(f"Failed to process image {url} for OCR: {e}")
                results.append("")
        
        print("OCR processing complete.")
        return results