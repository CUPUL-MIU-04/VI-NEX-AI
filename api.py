# api.py - VERSIÓN ESTABLE Y COMPATIBLE
import os
import uuid
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VI-NEX-AI Video Generator",
    description="Generador de videos con IA basado en Open-Sora",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sistema simple de API keys
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

# HTML embebido - no necesita Jinja2
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VI-NEX-AI - Generador de Video</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.2rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #60a5fa, #10b981);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .content {
            padding: 30px;
        }
        
        .form-section {
            background: #f9fafb;
            padding: 25px;
            border-radius: 15px;
            border: 1px solid #e5e7eb;
            margin-bottom: 20px;
        }
        
        .api-key-info {
            background: #fffbeb;
            border: 2px solid #fcd34d;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            font-size: 0.9rem;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #1f2937;
        }
        
        textarea {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            font-size: 16px;
            height: 120px;
            resize: vertical;
            font-family: inherit;
        }
        
        textarea:focus {
            outline: none;
            border-color: #6366f1;
        }
        
        .btn {
            background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
        }
        
        .btn:disabled {
            background: #6c757d;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #6366f1;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result-section {
            background: #f9fafb;
            padding: 25px;
            border-radius: 15px;
            border: 1px solid #e5e7eb;
            min-height: 200px;
        }
        
        .success {
            color: #10b981;
            text-align: center;
            padding: 20px;
        }
        
        .error {
            color: #ef4444;
            text-align: center;
            padding: 20px;
        }
        
        .processing {
            color: #f59e0b;
            text-align: center;
            padding: 20px;
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
                <div class="api-key-info">
                    <strong>🔑 API Key:</strong> Usa <code>demo_key_123456</code> para probar el servicio
                </div>

                <div class="form-group">
                    <label for="prompt">✨ Describe tu video</label>
                    <textarea 
                        id="prompt" 
                        placeholder="Ej: Un astronauta cabalgando un caballo galopante en el espacio profundo, nebulosas coloridas de fondo, estilo cinematográfico..."
                    ></textarea>
                </div>

                <button class="btn" onclick="generateVideo()" id="generateBtn">
                    <span id="btnText">🚀 Generar Video</span>
                </button>

                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <h3>Procesando tu video...</h3>
                    <p>Esta operación puede tomar unos momentos.</p>
                </div>
            </div>

            <div class="result-section">
                <h2>🎥 Resultado</h2>
                <div id="result">
                    <div style="text-align: center; color: #6b7280; padding: 40px 20px;">
                        <div style="font-size: 3rem; margin-bottom: 15px;">🎬</div>
                        <h3>Tu video aparecerá aquí</h3>
                        <p>Describe tu idea y haz clic en "Generar Video"</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_BASE_URL = window.location.origin;
        let currentJobId = null;

        async function generateVideo() {
            const prompt = document.getElementById('prompt').value.trim();
            const generateBtn = document.getElementById('generateBtn');
            const btnText = document.getElementById('btnText');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');

            // Validaciones
            if (!prompt) {
                alert('Por favor describe el video que quieres generar');
                return;
            }

            if (prompt.length < 5) {
                alert('La descripción debe tener al menos 5 caracteres');
                return;
            }

            // Actualizar UI
            generateBtn.disabled = true;
            btnText.textContent = '⏳ Iniciando...';
            loading.style.display = 'block';
            result.innerHTML = '<div class="processing"><div class="spinner"></div><h3>Iniciando generación...</h3></div>';

            try {
                const response = await fetch(API_BASE_URL + '/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: prompt,
                        api_key: 'demo_key_123456',
                        config: 'vi_nex_512px.py'
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    currentJobId = data.job_id;
                    result.innerHTML = `<div class="processing"><h3>✅ Solicitud aceptada</h3><p>ID del trabajo: ${data.job_id}</p></div>`;
                    checkJobStatus();
                } else {
                    throw new Error(data.detail || 'Error al generar video');
                }
            } catch (error) {
                showError(error.message);
                resetUI();
            }
        }

        async function checkJobStatus() {
            if (!currentJobId) return;

            try {
                const response = await fetch(API_BASE_URL + '/api/status/' + currentJobId);
                const data = await response.json();

                const result = document.getElementById('result');

                if (data.status === 'completed') {
                    result.innerHTML = `
                        <div class="success">
                            <h3>✅ ¡Video Generado Exitosamente!</h3>
                            <p><strong>Prompt:</strong> ${data.prompt}</p>
                            <p>🎉 ¡Tu API VI-NEX-AI está funcionando correctamente!</p>
                            <p><em>Modo demo: En producción se generaría un video real</em></p>
                            <button onclick="location.reload()" class="btn" style="margin-top: 15px; width: auto;">
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
                        <div class="processing">
                            <div class="spinner"></div>
                            <h3>🔄 ${data.message}</h3>
                            <p>Tiempo transcurrido: ${data.elapsed_seconds || 0} segundos</p>
                            <p>Progreso: ${data.progress || '50%'}</p>
                        </div>
                    `;
                    // Verificar de nuevo en 2 segundos
                    setTimeout(checkJobStatus, 2000);
                }
            } catch (error) {
                console.error('Error checking status:', error);
                // Reintentar después de error
                setTimeout(checkJobStatus, 3000);
            }
        }

        function showError(message) {
            const result = document.getElementById('result');
            result.innerHTML = `
                <div class="error">
                    <h3>❌ Error</h3>
                    <p>${message}</p>
                    <button onclick="location.reload()" class="btn" style="background: linear-gradient(135deg, #ef4444, #dc2626); margin-top: 15px; width: auto;">
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

        // Permitir Ctrl+Enter para generar
        document.getElementById('prompt').addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                generateVideo();
            }
        });

        // Enfocar el textarea al cargar
        document.getElementById('prompt').focus();
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
    
    # Validar API key
    if not validate_api_key(request.api_key):
        raise HTTPException(status_code=401, detail="API key inválida")
    
    # Validar prompt
    if not request.prompt or len(request.prompt.strip()) < 5:
        raise HTTPException(status_code=400, detail="El prompt debe tener al menos 5 caracteres")
    
    # Crear trabajo
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "processing",
        "prompt": request.prompt,
        "config": request.config,
        "created_at": time.time()
    }
    
    # Iniciar procesamiento en background
    background_tasks.add_task(process_video_generation, job_id)
    
    return JSONResponse({
        "job_id": job_id,
        "status": "processing",
        "message": "Video en proceso de generación",
        "estimated_time": "10-15 segundos",
        "check_status_url": f"/api/status/{job_id}"
    })

async def process_video_generation(job_id: str):
    """Procesar generación de video en modo demo"""
    try:
        logger.info(f"Procesando trabajo {job_id}")
        
        # Simular tiempo de procesamiento (8-12 segundos)
        processing_time = 8 + (hash(job_id) % 5)  # Entre 8-12 segundos
        await asyncio.sleep(processing_time)
        
        # Marcar como completado
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["completed_at"] = time.time()
        jobs[job_id]["processing_time"] = processing_time
        
        logger.info(f"Trabajo {job_id} completado exitosamente")
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        logger.error(f"Error en trabajo {job_id}: {e}")

@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    """Obtener estado del trabajo"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    
    job = jobs[job_id]
    elapsed_time = time.time() - job["created_at"]
    
    if job["status"] == "completed":
        return {
            "job_id": job_id,
            "status": "completed",
            "prompt": job["prompt"],
            "message": "¡Video generado exitosamente!",
            "processing_time": job.get("processing_time", 0),
            "total_time": round(elapsed_time, 2),
            "note": "Modo demo: En producción se generaría un video real con tu modelo VI-NEX-AI"
        }
    elif job["status"] == "failed":
        return {
            "job_id": job_id,
            "status": "failed",
            "error": job.get("error", "Error desconocido en la generación")
        }
    else:
        # Calcular progreso basado en tiempo transcurrido
        progress = min(85, int((elapsed_time / 12) * 100))  # Máximo 85% hasta completar
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Generando video con IA...",
            "elapsed_seconds": int(elapsed_time),
            "progress": f"{progress}%",
            "estimated_remaining": max(1, 12 - int(elapsed_time))
        }

@app.get("/api/configs")
async def get_available_configs():
    """Obtener configuraciones disponibles"""
    return [
        {
            "name": "vi_nex_512px", 
            "file": "vi_nex_512px.py", 
            "description": "Calidad estándar 512px - Balance perfecto"
        },
        {
            "name": "vi_nex_256px", 
            "file": "256px.py", 
            "description": "Rápido 256px - Para pruebas rápidas"
        },
        {
            "name": "vi_nex_768px", 
            "file": "768px.py", 
            "description": "Alta calidad 768px - Máxima resolución"
        },
    ]

@app.get("/health")
async def health_check():
    """Endpoint de salud del servicio"""
    return {
        "status": "healthy",
        "service": "VI-NEX-AI API",
        "version": "1.0.0",
        "timestamp": time.time(),
        "active_jobs": len([j for j in jobs.values() if j.get("status") == "processing"]),
        "total_jobs": len(jobs),
        "mode": "demo"
    }

@app.get("/test")
async def test_endpoint():
    """Endpoint de prueba simple"""
    return {
        "message": "¡VI-NEX-AI API está funcionando correctamente!",
        "status": "success",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
