_base_ = ["../vi_nex_512px.py"]

# 🎯 VI-NEX-AI: Configuración Ultra Larga (30-60 segundos)
video_duration_config = dict(
    max_duration_seconds=60,
    min_duration_seconds=30,
    target_duration_seconds=45,
    fps_target=15,              # FPS muy reducido
    variable_length=False,
    description="Videos ultra largos - VI-NEX-AI (requiere hardware potente)"
)

# 🚀 Optimizaciones extremas
sampling_option = dict(
    resolution="512px",         # Resolución reducida
    aspect_ratio="16:9",
    num_frames=675,             # 45 segundos @ 15fps
    fps_target=15,
    num_steps=100,              # Máxima calidad
    guidance=5.0,               # Guía mínima para coherencia
    text_osci=False,
    method="vi_nex_ultra_long", 
)
motion_score = "2"
fps_save = 15

# 💻 Paralelismo agresivo
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=4,
    sp_size=16,                 # Máximo sequence parallelism
    zero_stage=3,               # ZeRO stage 3 para ahorrar memoria
)

# 🤖 Modelo especializado
model = dict(
    type="vi_nex_flux_ultra",
    from_pretrained="./ckpts/vi_nex_ai_ultra_long.safetensors",
    max_sequence_length=2048,   # Secuencia ultra larga
)

save_dir = "vi_nex_samples_ultra_long"