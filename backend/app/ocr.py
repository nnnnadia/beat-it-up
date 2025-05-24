from fastapi import UploadFile
from PIL import Image
import pytesseract
import io

async def extract_text_from_image(file: UploadFile) -> str:
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    text = pytesseract.image_to_string(image, lang='por')
    return text