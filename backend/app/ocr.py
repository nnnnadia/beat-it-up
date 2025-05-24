from fastapi import UploadFile
from PIL import Image, ImageOps
import pytesseract
import io

async def extract_text_from_image(file: UploadFile) -> str:
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    # Preprocessing: convert to grayscale
    image = image.convert("L")
    # Preprocessing: apply simple thresholding
    image = image.point(lambda x: 0 if x < 140 else 255, '1')
    text = pytesseract.image_to_string(image, lang='por')
    return text