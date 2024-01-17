from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import librosa
import numpy as np
import os
from fastapi.middleware.cors import CORSMiddleware
# other imports
app = FastAPI()

# Add middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# rest of your code
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return FileResponse('./static/analyze.html')


@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Save the file temporarily
        with open(f"temp_{file.filename}", "wb") as buffer:
            buffer.write(file.file.read())

        # Load and process the file using Librosa
        y, sr = librosa.load(f"temp_{file.filename}", sr=None)
        duration = librosa.get_duration(y=y, sr=sr)

        # Optionally, perform additional processing here

        # Clean up: Delete the temporary file
        os.remove(f"temp_{file.filename}")

        return {"filename": file.filename, "duration": duration}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
