_base_ = ["../vi_nex_768px.py"]

# 🎯 VI-NEX-AI: Configuración Estándar (4-10 segundos)
video_duration_config = dict(
    max_duration_seconds=10,
    min_duration_seconds=4,
    target_duration_seconds=7,
    fps_target=24, 
    variable_length=True,
    description="Duración estándar para uso general - VI-NEX-AI"
)

# ⚖️ Configuración balanceada
sampling_option = dict(
    resolution="768px",
    aspect_ratio="16:9",
    num_frames=168,             # 7 segundos @ 24fps
    fps_target=24,
    num_steps=60,               # Sampling balanceado
    guidance=7.5,               # Guía estándar
    method="vi_nex_standard",
)
motion_score = "4"
fps_save = 24

save_dir = "vi_nex_samples_standard"