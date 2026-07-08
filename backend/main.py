import os 
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ai.classifier import classify_image

app = FastAPI(title="Media Analysis Web Demo")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Media Analysis Web Demo API!"}


@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = classify_image(file_path)

        file_size_kb = round(os.path.getsize(file_path) / 1024, 2)

        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_size_kb": file_size_kb,
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "message": "Uploaded file was processed locally and deleted after analysis."
        }
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


