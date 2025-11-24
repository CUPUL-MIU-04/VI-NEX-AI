import secrets
import hashlib
import json
from datetime import datetime, timedelta

def generate_user_api_key(user_id: str, expires_days: int = 90):
    """Genera API keys seguras para usuarios"""
    
    # Generar token seguro
    raw_token = secrets.token_urlsafe(32)
    
    # Crear hash para almacenar (nunca almacenes el token plano)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    
    api_key_info = {
        "user_id": user_id,
        "token_hash": token_hash,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=expires_days)).isoformat(),
        "permissions": ["video_generate", "video_download"]
    }
    
    print(f"✅ API Key generada para {user_id}:")
    print(f"🔑 Token: {raw_token}")
    print(f"📅 Expira: {api_key_info['expires_at']}")
    print("⚠️  GUARDA ESTE TOKEN - NO SE PODRÁ RECUPERAR")
    
    return raw_token, api_key_info

if __name__ == "__main__":
    user_id = input("Ingresa el ID de usuario: ")
    generate_user_api_key(user_id)
