from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# Fix potential import error if running from different dirs
try:
    from analyzer import analyze_code
except ImportError:
    from .analyzer import analyze_code

app = FastAPI(title="Code Smell Detector API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    sourceCode: str

@app.post("/api/analyze")
async def analyze_endpoint(request: CodeRequest):
    if not request.sourceCode.strip():
        raise HTTPException(status_code=400, detail="Source code cannot be empty")
    
    # Limit check (academic constraint)
    if len(request.sourceCode.splitlines()) > 500:
        raise HTTPException(status_code=400, detail="Source code exceeds 500 lines limit")

    result = analyze_code(request.sourceCode)
    return result

@app.get("/")
def read_root():
    return {"status": "active", "message": "Code Smell Detection API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
