from fastapi import UploadFile
from PIL import Image, ImageOps
import pytesseract
import io
import pandas as pd

async def extract_text_from_image(file: UploadFile) -> str:
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    # Preprocessing: convert to grayscale
    image = image.convert("L")
    # Preprocessing: apply simple thresholding
    image = image.point(lambda x: 0 if x < 140 else 255, '1')
    tsv = pytesseract.image_to_data(image, lang='por', output_type=pytesseract.Output.STRING)
    return tsv

async def extract_table_as_csv(file: UploadFile) -> str:
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image = image.convert("L")
    image = image.point(lambda x: 0 if x < 140 else 255, '1')
    # Get TSV output from Tesseract
    df = pytesseract.image_to_data(image, lang='por', output_type=pytesseract.Output.DATAFRAME)
    # Filter out rows without text
    df = df[df.text.notnull()]
    # Optionally, filter by block_num, line_num, etc. to get just the table
    # For now, return all detected text as CSV
    csv_data = df[['text']].to_csv(index=False, header=False)
    return csv_data