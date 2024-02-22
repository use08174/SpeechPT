from fastapi import FastAPI, Request, UploadFile, HTTPException, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

# Assuming `analyze_file` is correctly implemented in 'func.py'
from func import analyze_pt_file, analyze_sum_file

app = FastAPI(title='Speech Practice')

# Set base directory to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure templates directory
templates_directory = os.path.join(BASE_DIR, "frontend", "templates")
templates = Jinja2Templates(directory=templates_directory)

# Configure static files directory
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend", "static")), name="static") 

# Configure CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Temporary results storage
results = {}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/pt_upload/")
async def show_upload_page(request: Request):
    """Display upload page."""
    return templates.TemplateResponse("pt_upload.html", {"request": request})

@app.get("/sum_upload/")
async def show_upload_page(request: Request):
    """Display upload page."""
    return templates.TemplateResponse("sum_result.html", {"request": request})

@app.get("/member/")
async def show_upload_page(request: Request):
    """Display upload page."""
    return templates.TemplateResponse("member.html", {"request": request})

@app.post("/detect_pt/")
async def analyze_endpoint(file: UploadFile = File(...)):
    """Analyze uploaded file and return results."""
    try:
        # Ensure file is not empty
        if file.file:
            result = await analyze_pt_file(file)
            session_id = str(uuid.uuid4())
            results[session_id] = result  # Store result with session_id
        else:
            raise HTTPException(status_code=400, detail="No file uploaded or file is empty.")
    except Exception as e:
        return JSONResponse(content={"error": e}, status_code=500) ####str{e} -> {e}로 수정

    # Ensure result is serializable, consider converting result if it's a complex object
    print(result)
    return result



@app.post("/detect_sum/")
async def analyze_endpoint(file: UploadFile = File(...)):
    """Analyze uploaded file and return results."""
    try:
        # Ensure file is not empty
        if file.file:
            result = await analyze_sum_file(file)
            session_id = str(uuid.uuid4())
            results[session_id] = result  # Store result with session_id
        else:
            raise HTTPException(status_code=400, detail="No file uploaded or file is empty.")
    except Exception as e:
        return JSONResponse(content={"error": e}, status_code=500) ###str{e} -> e로 수정

    # Ensure result is serializable, consider converting result if it's a complex object
    print({"result": result, "session_id": session_id})
    return {"result": result, "session_id": session_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
