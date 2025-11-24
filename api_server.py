from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # Compatible con v1.10.13
import os
import uvicorn
import uuid

app = FastAPI(title="VI-NEX-AI API", version="1.0.0")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Keys
USER_API_KEYS = os.getenv("USER_API_KEYS", "test_key_123,demo_key_456").split(",")

class VideoRequest(BaseModel):
    prompt: str
    config: str = "vi_nex_512px.py"
    style: str = "default"

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in USER_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

@app.post("/generate-video")
async def generate_video(request: VideoRequest, api_key: str = Header(...)):
    """Endpoint simulado para generación de video"""
    job_id = str(uuid.uuid4())[:8]
    
    return {
        "job_id": job_id,
        "status": "processing", 
        "message": f"Video simulation started for: {request.prompt}",
        "config": request.config,
        "note": "API running on Render.com - Ready for VI-NEX-AI integration"
    }

@app.get("/health")
async def health_check(api_key: str = Header(...)):
    return {
        "status": "healthy", 
        "service": "VI-NEX-AI API",
        "version": "1.0.0",
        "environment": "render.com"
    }

@app.get("/")
async def root():
    return {
        "message": "VI-NEX-AI API is running successfully on Render.com!",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
