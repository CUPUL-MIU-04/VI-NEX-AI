# api_server.py
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI(title="VI-NEX-AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USER_API_KEYS = os.getenv("USER_API_KEYS", "test_key_123").split(",")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in USER_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

@app.post("/generate-video")
async def generate_video(prompt: str, api_key: str = Header(...)):
    return {
        "job_id": "demo_123",
        "status": "success", 
        "message": f"Video simulation: {prompt}",
        "note": "API is working! Integrate your VI-NEX-AI model here."
    }

@app.get("/health")
async def health_check(api_key: str = Header(...)):
    return {"status": "healthy", "service": "VI-NEX-AI"}

@app.get("/")
async def root():
    return {"message": "VI-NEX-AI API Running on Render"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
