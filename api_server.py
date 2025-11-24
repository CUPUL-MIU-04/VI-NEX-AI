from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI(title="VI-NEX-AI API")

# Configuración desde secrets
VI_NEX_API_TOKENS = os.getenv("VI_NEX_API_TOKENS", "").split(",")
GITHUB_TOKEN = os.getenv("VI_NEX_API_TOKEN")  # Tu fine-grained token

async def verify_api_key(api_key: str = Header(..., alias="X-API-Key")):
    """Verifica las API keys de usuarios"""
    if api_key not in VI_NEX_API_TOKENS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

def verify_github_access():
    """Verifica acceso al repositorio usando el fine-grained token"""
    if not GITHUB_TOKEN:
        return False
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(
            "https://api.github.com/repos/CUPUL-MIU-04/VI-NEX-AI",
            headers=headers
        )
        return response.status_code == 200
    except:
        return False

@app.post("/generate-video")
async def generate_video(
    prompt: str,
    config: str = "vi_nex_512px.py",
    api_key: str = Depends(verify_api_key)
):
    # Verificar acceso a GitHub
    if not verify_github_access():
        raise HTTPException(
            status_code=500, 
            detail="GitHub access not configured properly"
        )
    
    # Tu lógica de generación de video aquí
    return {
        "status": "success", 
        "message": "Video generation started",
        "config": config
    }

@app.get("/system/health")
async def health_check():
    github_access = verify_github_access()
    return {
        "status": "healthy",
        "github_access": github_access,
        "service": "VI-NEX-AI"
    }
