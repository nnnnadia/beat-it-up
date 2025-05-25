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

async def extract_table_as_objects(file: UploadFile):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image = image.convert("L")
    image = image.point(lambda x: 0 if x < 140 else 255, '1')
    df = pytesseract.image_to_data(image, lang='por', output_type=pytesseract.Output.DATAFRAME)
    df = df[df.text.notnull()]

    # Group by line number and join words in each line
    lines = df.groupby('line_num')['text'].apply(lambda x: ' '.join(x)).tolist()
    # Remove header or empty lines
    lines = [line for line in lines if line.strip() and not line.lower().startswith("exercício")]

    result = []
    for line in lines:
        parts = line.split()
        if len(parts) < 3:
            continue  # skip lines that don't look like table rows
        # Assume last two columns are series and repetition, rest is name
        try:
            series = int(parts[-2])
            repetition = int(parts[-1].replace(',', '').replace('.', ''))
            name = ' '.join(parts[:-2])
            result.append({
                "name": name,
                "series": series,
                "repetition": repetition
            })
        except ValueError:
            continue  # skip if conversion fails

    return result