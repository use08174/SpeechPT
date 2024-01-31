from fastapi import FastAPI, Request, File, UploadFile
import os
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from func import analyze_file


app = FastAPI(project_name='speech_practice')

@app.post("/detect/")
async def analyze_endpoint(file: UploadFile):
    return await analyze_file(file)

