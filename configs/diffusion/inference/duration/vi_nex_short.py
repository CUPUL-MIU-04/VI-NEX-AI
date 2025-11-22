_base_ = ["../vi_nex_512px.py"]

# 🎯 VI-NEX-AI: Configuración para Videos Cortos (2-5 segundos)
video_duration_config = dict(
    max_duration_seconds=5,
    min_duration_seconds=2,
    target_duration_seconds=3,
    fps_target=24,
    variable_length=True,
    description="Videos cortos optimizados para redes sociales - VI-NEX-AI"
)

# ⚡ Optimizaciones para velocidad
sampling_option = dict(
    resolution="512px",
    aspect_ratio="16:9", 
    num_frames=72,              # 3 segundos @ 24fps
    fps_target=24,
    num_steps=30,               # Sampling rápido
    guidance=6.0,               # Guía balanceada
    method="vi_nex_fast",
)
motion_score = "3"
fps_save = 24

# 🤖 Modelo optimizado para velocidad
model = dict(
    type="vi_nex_flux_fast",
    from_pretrained="./ckpts/vi_nex_ai_fast.safetensors",
    hidden_size=2048,           # Modelo más pequeño
    depth=16,
)

# 💨 Sin paralelismo para máxima velocidad
plugin = None
plugin_config = None

save_dir = "vi_nex_samples_short"