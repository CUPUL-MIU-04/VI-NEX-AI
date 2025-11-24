from fastapi import FastAPI, HTTPException, Header, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uvicorn
import uuid
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

@app.post("/generate-video")
async def generate_video(
    prompt: str = Form(...),
    config: str = Form("vi_nex_512px.py"),
    style: str = Form("default"),
    api_key: str = Header(..., alias="api-key")
):
    if api_key not in USER_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    job_id = str(uuid.uuid4())[:8]
    
    # Simulación mejorada - en producción aquí iría tu modelo real
    print(f"🎬 Simulando generación: {prompt}")
    
    return {
        "job_id": job_id,
        "status": "completed", 
        "message": f"Video simulado generado para: {prompt}",
        "video_url": f"/sample-video",  # Ruta para video de ejemplo
        "note": "Modo simulación - Integra tu modelo VI-NEX-AI aquí"
    }

# Ruta para servir un video de ejemplo
@app.get("/sample-video")
async def get_sample_video():
    # Puedes poner un video de ejemplo en tu repositorio
    sample_path = "assets/sample_video.mp4"
    
    if os.path.exists(sample_path):
        return FileResponse(sample_path, media_type='video/mp4', filename="sample_video.mp4")
    else:
        # Si no hay video, redirigir a un video online de ejemplo
        return {"video_url": "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"}

@app.get("/health")
async def health_check(api_key: str = Header(..., alias="api-key")):
    return {
        "status": "healthy", 
        "service": "VI-NEX-AI",
        "mode": "simulation"
    }

@app.get("/")
async def root():
    return {"message": "VI-NEX-AI API - Modo Simulación"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
