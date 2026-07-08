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

@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    # 1. Restrict format to .wav or .mp3 to demonstrate file validation
    if not file.filename.endswith(('.wav', '.mp3')):
        raise HTTPException(status_code=400, detail="Invalid audio format. Please upload a .wav or .mp3 file.")
    
    # 2. Local variable paths for secure local storage
    temp_file_path = f"temp_{file.filename}"
    
    try:
        # Save file chunks asynchronously to handle network streams smoothly
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # --- THE FRAUNHOFER SIMULATION LAYER ---
        # In a production environment, this is where we feed the file into Librosa
        # to generate a 2D Mel-Spectrogram matrix and trigger TensorFlow inference.
        file_size_kb = round(os.path.getsize(temp_file_path) / 1024, 2)
        
        # Simulate an advanced audio manipulation result payload
        analysis_result = {
            "filename": file.filename,
            "type": file.content_type,
            "size": f"{file_size_kb} KB",
            "prediction": "Synthetic Speech (AI Generated Clone)",
            "confidence": "94.21%",
            "anomalies_detected": [
                {"timestamp": "00:02.15", "type": "Phase Inconsistency"},
                {"timestamp": "00:05.40", "type": "High-Frequency Upsampling Artifact"}
            ]
        }
        return analysis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # 3. Secure local cleanup - matching your Data Privacy Flex!
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

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


