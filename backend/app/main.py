from fastapi import FastAPI, UploadFile, File
from .ocr import extract_text_from_image

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    text = await extract_text_from_image(file)
    return {"text": text}