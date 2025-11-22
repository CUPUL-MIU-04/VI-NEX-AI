_base_ = ["../vi_nex_768px.py"]

# 🎯 VI-NEX-AI: Configuración para Videos Largos (10-30 segundos)
video_duration_config = dict(
    max_duration_seconds=30,
    min_duration_seconds=10,
    target_duration_seconds=20,
    fps_target=20,              # FPS reducido
    variable_length=False,      # Longitud fija
    description="Videos largos para contenido extendido - VI-NEX-AI"
)

# 🕒 Optimizaciones para duración extendida
sampling_option = dict(
    resolution="768px",
    aspect_ratio="16:9",
    num_frames=400,             # 20 segundos @ 20fps
    fps_target=20,
    num_steps=80,               # Más pasos para calidad
    guidance=6.5,               # Guía reducida para coherencia
    text_osci=False,            # Sin oscilación para estabilidad
    method="vi_nex_long",
)
motion_score = "3"
fps_save = 20

# 💾 Paralelismo para secuencias largas
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=2,
    sp_size=8,                  # Más sequence parallelism
    zero_stage=2,
)

# 🤖 Modelo optimizado para secuencias largas
model = dict(
    type="vi_nex_flux_long", 
    from_pretrained="./ckpts/vi_nex_ai_long.safetensors",
    max_sequence_length=1024,   # Secuencia más larga
)

save_dir = "vi_nex_samples_long"