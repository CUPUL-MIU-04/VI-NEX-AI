# api_proxy.py - Versión ligera para Render.com
import os
import uuid
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx
import json
import logging
from pathlib import Path
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VI-NEX-AI Proxy API",
    description="Proxy para generación de videos con IA",
    version="1.0.0"
)

# Configuración CORS
ALLOWED_ORIGINS = [
    "https://vi-nex-ai.netlify.app",
    "https://vi-nex-ai.onrender.com",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="templates")

# Sistema de API keys
API_KEYS = {
    "demo": "demo_key_123456",
    "admin": os.getenv("ADMIN_API_KEY", "admin_key_789012")
}

# Almacenamiento en memoria
jobs = {}

class GenerateRequest(BaseModel):
    prompt: str
    api_key: str = "demo_key_123456"
    config: str = "vi_nex_512px.py"

def validate_api_key(api_key: str) -> bool:
    return api_key in API_KEYS.values()

async def call_external_ai_service(prompt: str, config: str):
    """
    En una implementación real, aquí llamarías a:
    - Google Colab con ngrok
    - AWS Lambda con GPU
    - Modal.com
    - Otro servicio con capacidad de GPU
    """
    # Por ahora simulamos la generación
    await asyncio.sleep(10)  # Simular procesamiento
    
    # En producción, reemplazar con llamada real a tu servicio de IA
    # Ejemplo:
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         "https://tu-servicio-ia-real.com/generate",
    #         json={"prompt": prompt, "config": config},
    #         timeout=300
    #     )
    #     return response.json()
    
    return {
        "success": True,
        "video_url": "https://example.com/generated-video.mp4",
        "status": "completed"
    }

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate")
async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
    """Endpoint para generar videos - Versión Proxy"""
    
    if not validate_api_key(request.api_key):
        raise HTTPException(status_code=401, detail="API key inválida")
    
    if not request.prompt or len(request.prompt.strip()) < 5:
        raise HTTPException(status_code=400, detail="El prompt debe tener al menos 5 caracteres")
    
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "processing",
        "prompt": request.prompt,
        "config": request.config,
        "created_at": time.time()
    }
    
    # En background, llamar al servicio real de IA
    background_tasks.add_task(process_video_generation, job_id, request.prompt, request.config)
    
    return JSONResponse({
        "job_id": job_id,
        "status": "processing", 
        "message": "Solicitud recibida - Procesando en servidor de IA...",
        "estimated_time": "2-5 minutos",
        "check_status_url": f"/api/status/{job_id}"
    })

async def process_video_generation(job_id: str, prompt: str, config: str):
    """Procesar generación llamando a servicio externo"""
    try:
        result = await call_external_ai_service(prompt, config)
        
        if result.get("success"):
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["video_url"] = result["video_url"]
        else:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = result.get("error", "Error en generación")
            
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        logger.error(f"Error procesando trabajo {job_id}: {e}")

@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    
    job = jobs[job_id]
    
    if job["status"] == "completed":
        return {
            "job_id": job_id,
            "status": "completed",
            "video_url": job["video_url"],
            "prompt": job["prompt"]
        }
    elif job["status"] == "failed":
        return {
            "job_id": job_id,
            "status": "failed", 
            "error": job.get("error", "Error desconocido")
        }
    else:
        elapsed = time.time() - job["created_at"]
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Generando video en servidor de IA...",
            "elapsed_seconds": int(elapsed)
        }

@app.get("/api/configs")
async def get_available_configs():
    """Configuraciones disponibles"""
    return [
        {"name": "vi_nex_512px", "file": "vi_nex_512px.py", "description": "Calidad estándar 512px"},
        {"name": "vi_nex_256px", "file": "256px.py", "description": "Rápido 256px"},
        {"name": "vi_nex_768px", "file": "768px.py", "description": "Alta calidad 768px"},
    ]

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "VI-NEX-AI Proxy",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
