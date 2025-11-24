from fastapi import FastAPI, HTTPException, Header, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import sys
from pathlib import Path

app = FastAPI(title="VI-NEX-AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USER_API_KEYS = os.getenv("USER_API_KEYS", "test_key_123,user_key_456").split(",")

# Función para verificar el estado del modelo
def check_model_status():
    """Verifica si el modelo puede generar videos"""
    try:
        # Intenta importar componentes básicos
        sys.path.append('.')
        from opensora.utils.config import load_config
        
        config_path = "configs/diffusion/inference/vi_nex_256px.py"
        if os.path.exists(config_path):
            config = load_config(config_path)
            return {
                "status": "config_loaded",
                "message": "Configuración cargada correctamente",
                "model_ready": False,  # Cambiar a True cuando integres el modelo real
                "config": config_path
            }
        else:
            return {
                "status": "config_missing", 
                "message": "Archivo de configuración no encontrado",
                "model_ready": False
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al cargar modelo: {str(e)}",
            "model_ready": False
        }

@app.post("/generate-video")
async def generate_video(
    prompt: str = Form(...),
    config: str = Form("vi_nex_512px.py"),
    style: str = Form("default"),
    api_key: str = Header(..., alias="api-key")
):
    if api_key not in USER_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    # Verificar estado del modelo
    model_status = check_model_status()
    
    if not model_status["model_ready"]:
        # Modo simulación con información del modelo
        return {
            "job_id": "simulation_" + prompt[:10].replace(" ", "_"),
            "status": "simulation", 
            "message": f"Descripción recibida: '{prompt}'",
            "model_status": model_status,
            "note": "El modelo no está integrado aún. Esto es una simulación.",
            "expected_config": config,
            "expected_style": style
        }
    
    # Aquí iría la generación real cuando el modelo esté listo
    # try:
    #     video_path = generate_real_video(prompt, config, style)
    #     return {"video_url": video_path, "status": "completed"}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error en generación: {str(e)}")

@app.get("/health")
async def health_check(api_key: str = Header(..., alias="api-key")):
    model_status = check_model_status()
    
    return {
        "status": "healthy", 
        "service": "VI-NEX-AI",
        "model_status": model_status,
        "api_ready": True,
        "model_ready": model_status["model_ready"]
    }

@app.get("/model-status")
async def model_status(api_key: str = Header(..., alias="api-key")):
    """Endpoint específico para verificar el estado del modelo"""
    return check_model_status()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
