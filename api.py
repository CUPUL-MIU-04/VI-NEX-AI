# api.py
import os
import uuid
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import subprocess
import json
import logging
from pathlib import Path
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VI-NEX-AI Video Generator",
    description="Generador de videos con IA basado en Open-Sora modificado",
    version="1.0.0"
)

# Configuración CORS para permitir tu frontend de Netlify
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

# Directorios - en Render usamos /tmp
BASE_DIR = Path(__file__).parent
VIDEOS_DIR = Path("/tmp/generated_videos")
TEMP_DIR = Path("/tmp/temp")

VIDEOS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Montar directorio estático para videos
app.mount("/videos", StaticFiles(directory=VIDEOS_DIR), name="videos")

# Templates para el frontend
templates = Jinja2Templates(directory="templates")

# Sistema simple de API keys
API_KEYS = {
    "demo": "demo_key_123456",
    "admin": os.getenv("ADMIN_API_KEY", "admin_key_789012")
}

# Almacenamiento en memoria de trabajos
jobs = {}

class GenerateRequest(BaseModel):
    prompt: str
    api_key: str = "demo_key_123456"
    config: str = "vi_nex_512px.py"

def validate_api_key(api_key: str) -> bool:
    return api_key in API_KEYS.values()

def run_vi_nex_inference(prompt: str, config: str, output_path: str):
    """Ejecuta la generación de video usando tu modelo VI-NEX-AI"""
    try:
        logger.info(f"Iniciando generación de video: {prompt}")
        
        # Usar el script de inferencia de tu proyecto
        cmd = [
            "python", "scripts/diffusion/inference.py",
            "--config", f"configs/diffusion/inference/{config}",
            "--prompt", prompt,
            "--save_path", output_path,
            "--fps", "24"
        ]
        
        logger.info(f"Comando: {' '.join(cmd)}")
        
        # Ejecutar el proceso
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=300  # 5 minutos timeout
        )
        
        if process.returncode == 0:
            logger.info("Video generado exitosamente")
            return True
        else:
            logger.error(f"Error en generación: {process.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("Timeout en generación de video")
        return False
    except Exception as e:
        logger.error(f"Excepción en generación: {e}")
        return False

async def process_video_generation(job_id: str, prompt: str, config: str):
    """Procesar generación de video en background"""
    try:
        output_path = VIDEOS_DIR / f"{job_id}.mp4"
        
        # Ejecutar en thread separado para no bloquear
        success = await asyncio.get_event_loop().run_in_executor(
            None, 
            run_vi_nex_inference, 
            prompt, config, str(output_path)
        )
        
        if success and output_path.exists():
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["output_path"] = str(output_path)
            jobs[job_id]["completed_at"] = time.time()
        else:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = "Error en la generación del video"
            
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        logger.error(f"Error procesando trabajo {job_id}: {e}")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate")
async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
    """Endpoint para generar videos"""
    
    # Validar API key
    if not validate_api_key(request.api_key):
        raise HTTPException(status_code=401, detail="API key inválida")
    
    # Validar prompt
    if not request.prompt or len(request.prompt.strip()) < 5:
        raise HTTPException(status_code=400, detail="El prompt debe tener al menos 5 caracteres")
    
    # Validar configuración
    config_path = BASE_DIR / "configs" / "diffusion" / "inference" / request.config
    if not config_path.exists():
        raise HTTPException(status_code=400, detail="Configuración no válida")
    
    # Crear trabajo
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "processing",
        "prompt": request.prompt,
        "config": request.config,
        "created_at": time.time()
    }
    
    # Ejecutar en background
    background_tasks.add_task(process_video_generation, job_id, request.prompt, request.config)
    
    return JSONResponse({
        "job_id": job_id,
        "status": "processing",
        "message": "Video en proceso de generación",
        "estimated_time": "2-5 minutos",
        "check_status_url": f"/api/status/{job_id}"
    })

@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    """Obtener estado del trabajo"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    
    job = jobs[job_id]
    
    if job["status"] == "completed":
        video_filename = f"{job_id}.mp4"
        return {
            "job_id": job_id,
            "status": "completed",
            "video_url": f"/videos/{video_filename}",
            "prompt": job["prompt"],
            "config": job["config"]
        }
    elif job["status"] == "failed":
        return {
            "job_id": job_id,
            "status": "failed",
            "error": job.get("error", "Error desconocido")
        }
    else:
        # Calcular tiempo transcurrido
        elapsed = time.time() - job["created_at"]
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Generando video...",
            "elapsed_seconds": int(elapsed)
        }

@app.get("/api/configs")
async def get_available_configs():
    """Obtener configuraciones disponibles"""
    configs_dir = BASE_DIR / "configs" / "diffusion" / "inference"
    configs = []
    
    try:
        for file in configs_dir.iterdir():
            if file.name.startswith(("vi_nex", "256px", "768px")) and file.suffix == ".py":
                config_name = file.stem
                configs.append({
                    "name": config_name,
                    "file": file.name,
                    "description": f"Configuración {config_name}"
                })
    except Exception as e:
        logger.error(f"Error leyendo configuraciones: {e}")
    
    return configs

@app.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {
        "status": "healthy", 
        "service": "VI-NEX-AI",
        "timestamp": time.time(),
        "active_jobs": len([j for j in jobs.values() if j["status"] == "processing"])
    }

@app.get("/docs")
async def get_docs():
    """Redireccionar a la documentación API"""
    return FileResponse("templates/index.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
