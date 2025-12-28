import sys
import os

# 1. Force add current directory to sys.path to resolve local imports (analyzer, smells)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import traceback

# Safe Import with debug
try:
    from analyzer import analyze_code
except ImportError as e:
    import_error = str(e)
    def analyze_code(code):
        raise Exception(f"Import Error: {import_error}. Sys Path: {sys.path}")

app = FastAPI(title="Code Smell Detector API")

# Enable CORS for everyone
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    sourceCode: str

@app.post("/api/analyze")
@app.post("/analyze")
async def analyze_endpoint(request: CodeRequest):
    try:
        if not request.sourceCode.strip():
            raise HTTPException(status_code=400, detail="Source code cannot be empty")
        
        if len(request.sourceCode.splitlines()) > 500:
            raise HTTPException(status_code=400, detail="Source code exceeds 500 lines limit")

        result = analyze_code(request.sourceCode)
        return result
    except Exception as e:
        # Return 500 with the specific error to show in Frontend
        return JSONResponse(status_code=500, content={"detail": f"Runtime Error: {str(e)}", "trace": traceback.format_exc()})

@app.get("/api")
def api_root():
    return {"status": "ok", "message": "API is reachable. Modules loaded."}

@app.options("/{path:path}")
async def options_handler(path: str):
    return {"status": "ok"}

# DEBUG: Catch-all for 404s to give us info
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path_name: str):
    return JSONResponse(
        status_code=404,
        content={
            "detail": f"Route not found. You requested: {path_name}",
            "method": request.method,
            "url": str(request.url)
        }
    )
