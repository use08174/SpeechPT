from fastapi import FastAPI, Request, File, UploadFile, HTTPException
import os
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_directory = os.path.join(BASE_DIR, "tests")
templates = Jinja2Templates(directory="../../frontend/templates")

from fastapi.middleware.cors import CORSMiddleware
import uuid

from func import analyze_file

# 상대 경로를 사용하여 templates 폴더 위치 설정
#templates=Jinja2Templates(directory="./../tests")

# 임시 결과 저장소
results={}

app = FastAPI(project_name='speech_practice')

# Add middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def read_root(request:Request):
    # index.html 렌더링
    return templates.TemplateResponse("index.html",{"request":request})

@app.post("/detect/")
async def analyze_endpoint(request:Request, file:UploadFile= File(...)):
    result=await analyze_file(file)
    
    session_id = str(uuid.uuid4())
    results[session_id] =result
    
    # 결과 페이지로 리디렉션
    return RedirectResponse(url=f"/result/{session_id}", status_code=303)

@app.get("/result/{session_id}", response_class=HTMLResponse)
async def show_result(request: Request, session_id: str):
    result = results.get(session_id, None)
    if result is None:
        raise HTTPException(status_code=404, detail="결과를 찾을 수 없습니다.")
    
    return templates.TemplateResponse("result.html", {"request": request, "result_data": result})

'''@app.get("/")
async def read_root():
    return FileResponse('backend/tests/index.html')

@app.post("/detect/")
async def analyze_endpoint(file: UploadFile):
    return await analyze_file(file)'''
 

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)