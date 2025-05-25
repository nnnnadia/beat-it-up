from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .ocr import extract_table_as_objects

app = FastAPI()

# Allow CORS for both local and production frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5173/beat-it-up/",
        "https://nnnnadia.github.io",
        "https://nnnnadia.github.io/beat-it-up/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    table = await extract_table_as_objects(file)
    return {"table": table}
