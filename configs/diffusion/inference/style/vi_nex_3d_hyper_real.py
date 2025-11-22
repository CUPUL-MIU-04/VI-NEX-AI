_base_ = ["../vi_nex_1024px.py"]

# 🎬 VI-NEX-AI: 3D HIPERREALISTA
style_config = dict(
    style_preset="hyper_real_3d",       # 3D hiperrealista
    art_style="photorealistic_cgi",     # CGI fotorrealista
    animation_type="hyper_realistic",   # Render hiperrealista
    rendering_quality="ultra",          # Calidad ultra
    lighting_model="path_tracing",      # Iluminación por path tracing
    material_quality="ultra",           # Materiales ultra realistas
    description="Animación 3D hiperrealista con iluminación por path tracing - VI-NEX-AI"
)

sampling_option = dict(
    resolution="1024px",
    aspect_ratio="16:9",
    num_frames=150,                     # Más corto por la complejidad
    fps_target=24,
    num_steps=120,                      # Máximos pasos para detalles
    guidance=9.5,                       # Guía máxima
    method="vi_nex_3d_hyper_real",
    photorealism_strength=0.95,         # Fuerza de fotorrealismo
    detail_preservation=1.0,            # Preservación máxima de detalles
)
motion_score = "3"                      # Movimiento realista

model = dict(
    type="vi_nex_flux_3d_hyper_real",
    from_pretrained="./ckpts/vi_nex_ai_3d_hyper_real.safetensors",
    hyper_realistic_enhancement=True,   # Mejoras hiperrealistas
    advanced_lighting=True,             # Iluminación avanzada
    global_illumination=True,           # Iluminación global
    ray_tracing_simulation=True,        # Simulación de ray tracing
)

save_dir = "vi_nex_samples_3d_hyper_real"