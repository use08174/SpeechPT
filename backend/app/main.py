from fastapi import FastAPI, Request, File, UploadFile
import os
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from func import analyze_file


app = FastAPI(project_name='speech_practice')

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


@app.get('/', response_class=HTMLResponse)  # connect the file received form the frontend
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "Rahul"})


@app.post("/detect/")
async def analyze_endpoint(file: UploadFile):
    return await analyze_file(file)
