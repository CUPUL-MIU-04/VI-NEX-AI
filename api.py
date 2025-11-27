# api.py - VERSIÓN SIN JINJA2
import os
import uuid
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel
import json
import logging
from pathlib import Path
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VI-NEX-AI Video Generator",
    description="Generador de videos con IA",
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

# Directorios
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

# Crear directorio static si no existe
STATIC_DIR.mkdir(exist_ok=True)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Sistema de API keys
API_KEYS = {
    "demo": "demo_key_123456",
    "admin": os.getenv("ADMIN_API_KEY", "admin_key_789012")
}

jobs = {}

class GenerateRequest(BaseModel):
    prompt: str
    api_key: str = "demo_key_123456"
    config: str = "vi_nex_512px.py"

def validate_api_key(api_key: str) -> bool:
    return api_key in API_KEYS.values()

# HTML directamente en el código como fallback
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VI-NEX-AI - Generador de Video</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 20px;
        }
        .container {
            max-width: 800px; margin: 0 auto; background: white;
            border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
            color: white; padding: 40px; text-align: center;
        }
        .header h1 {
            font-size: 2.5rem; margin-bottom: 10px;
            background: linear-gradient(135deg, #60a5fa, #10b981);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .content { padding: 40px; }
        .form-section {
            background: #f9fafb; padding: 30px; border-radius: 15px;
            border: 1px solid #e5e7eb; margin-bottom: 20px;
        }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #1f2937; }
        input, textarea {
            width: 100%; padding: 12px 16px; border: 2px solid #e5e7eb;
            border-radius: 10px; font-size: 16px;
        }
        textarea { height: 120px; resize: vertical; }
        .btn {
            background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
            color: white; border: none; padding: 15px 30px; border-radius: 10px;
            font-size: 16px; font-weight: 600; cursor: pointer; width: 100%;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn:disabled { background: #6c757d; cursor: not-allowed; transform: none; }
        .loading { display: none; text-align: center; padding: 30px; }
        .spinner {
            border: 4px solid #f3f3f3; border-top: 4px solid #6366f1;
            border-radius: 50%; width: 50px; height: 50px;
            animation: spin 1s linear infinite; margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); }
        }
        .result-section {
            background: #f9fafb; padding: 30px; border-radius: 15px;
            border: 1px solid #e5e7eb;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 VI-NEX-AI Video Generator</h1>
            <p>Potenciado por tu modelo modificado de Open-Sora</p>
        </div>
        <div class="content">
            <div class="form-section">
                <div style="background: #fffbeb; border: 2px solid #fcd34d; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                    <strong>🔑 API Key:</strong> Usa <code>demo_key_123456</code> para probar
                </div>
                <div class="form-group">
                    <label for="prompt">✨ Describe tu video</label>
                    <textarea id="prompt" placeholder="Ej: Un astronauta en el espacio..."></textarea>
                </div>
                <button class="btn" onclick="generateVideo()" id="generateBtn">
                    <span id="btnText">🚀 Generar Video</span>
                </button>
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <h3>Procesando tu video...</h3>
                    <p>Esta operación puede tomar de 2 a 5 minutos.</p>
                </div>
            </div>
            <div class="result-section">
                <h2>🎥 Resultado del Video</h2>
                <div id="result">
                    <div style="text-align: center; color: #6b7280; padding: 40px 20px;">
                        <div style="font-size: 3rem; margin-bottom: 20px;">🎬</div>
                        <h3>Tu video aparecerá aquí</h3>
                        <p>Describe tu idea y haz clic en "Generar Video"</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_BASE_URL = window.location.origin;
        
        async function generateVideo() {
            const prompt = document.getElementById('prompt').value.trim();
            const generateBtn = document.getElementById('generateBtn');
            const btnText = document.getElementById('btnText');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');

            if (!prompt) {
                alert('Por favor describe el video que quieres generar');
                return;
            }

            generateBtn.disabled = true;
            btnText.textContent = '⏳ Iniciando...';
            loading.style.display = 'block';
            result.innerHTML = '<div style="text-align: center;"><div class="spinner"></div><h3>Iniciando generación...</h3></div>';

            try {
                const response = await fetch(API_BASE_URL + '/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        prompt: prompt,
                        api_key: 'demo_key_123456',
                        config: 'vi_nex_512px.py'
                    })
                });

                const data = await response.json();
                if (response.ok) {
                    checkJobStatus(data.job_id);
                } else {
                    throw new Error(data.detail || 'Error al generar video');
                }
            } catch (error) {
                showError(error.message);
                resetUI();
            }
        }

        async function checkJobStatus(jobId) {
            const result = document.getElementById('result');
            
            try {
                const response = await fetch(API_BASE_URL + '/api/status/' + jobId);
                const data = await response.json();

                if (data.status === 'completed') {
                    result.innerHTML = `
                        <div style="text-align: center; color: #10b981;">
                            <h3>✅ ¡Video Generado Exitosamente!</h3>
                            <p><strong>Prompt:</strong> ${data.prompt}</p>
                            <p>🎉 ¡Funciona! Tu API VI-NEX-AI está ejecutándose correctamente.</p>
                            <p><em>Nota: En modo demo se simula la generación</em></p>
                            <button onclick="location.reload()" class="btn" style="margin-top: 20px;">
                                🎬 Generar Otro Video
                            </button>
                        </div>
                    `;
                    resetUI();
                } else if (data.status === 'failed') {
                    showError(data.error);
                    resetUI();
                } else {
                    result.innerHTML = `
                        <div style="text-align: center; color: #f59e0b;">
                            <div class="spinner" style="border-top-color: #f59e0b;"></div>
                            <h3>🔄 Generando video...</h3>
                            <p>${data.message}</p>
                            <p><small>Tiempo transcurrido: ${data.elapsed_seconds || 0}s</small></p>
                        </div>
                    `;
                    setTimeout(() => checkJobStatus(jobId), 2000);
                }
            } catch (error) {
                showError('Error verificando estado: ' + error.message);
                resetUI();
            }
        }

        function showError(message) {
            const result = document.getElementById('result');
            result.innerHTML = `
                <div style="color: #ef4444; text-align: center; padding: 20px;">
                    <h3>❌ Error</h3>
                    <p>${message}</p>
                    <button onclick="location.reload()" class="btn" style="background: linear-gradient(135deg, #ef4444, #dc2626);">
                        🔄 Reintentar
                    </button>
                </div>
            `;
        }

        function resetUI() {
            document.getElementById('generateBtn').disabled = false;
            document.getElementById('btnText').textContent = '🚀 Generar Video';
            document.getElementById('loading').style.display = 'none';
        }

        document.getElementById('prompt').addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                generateVideo();
            }
        });
    </script>
</body>
</html>
"""

@app.get("/")
async def read_root():
    return HTMLResponse(HTML_CONTENT)

@app.post("/api/generate")
async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
    """Endpoint para generar videos - Modo Demo"""
    
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
    
    # Simular procesamiento en background
    background_tasks.add_task(simulate_video_generation, job_id)
    
    return JSONResponse({
        "job_id": job_id,
        "status": "processing",
        "message": "Video en proceso de generación (Demo Mode)",
        "estimated_time": "10 segundos",
        "check_status_url": f"/api/status/{job_id}"
    })

async def simulate_video_generation(job_id: str):
    """Simular generación de video para demo"""
    try:
        # Esperar 5-10 segundos para simular procesamiento
        await asyncio.sleep(8)
        jobs[job_id]["status"] = "completed"
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        logger.error(f"Error en generación simulada: {e}")

@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    
    job = jobs[job_id]
    
    if job["status"] == "completed":
        return {
            "job_id": job_id,
            "status": "completed", 
            "prompt": job["prompt"],
            "message": "¡Generación completada! (Modo Demo)",
            "note": "En producción, aquí estaría la URL del video generado"
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
            "elapsed_seconds": int(elapsed),
            "progress": f"{min(80, int(elapsed * 10))}%"
        }

@app.get("/api/configs")
async def get_available_configs():
    return [
        {"name": "vi_nex_512px", "file": "vi_nex_512px.py", "description": "Calidad estándar 512px"},
        {"name": "vi_nex_256px", "file": "256px.py", "description": "Rápido 256px"}, 
        {"name": "vi_nex_768px", "file": "768px.py", "description": "Alta calidad 768px"},
    ]

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "VI-NEX-AI",
        "timestamp": time.time(),
        "version": "1.0.0",
        "mode": "demo"
    }

@app.get("/test")
async def test_endpoint():
    return {"message": "¡API funcionando correctamente!", "status": "success"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
