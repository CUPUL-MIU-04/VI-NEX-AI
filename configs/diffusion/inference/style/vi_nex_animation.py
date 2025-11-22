_base_ = ["../vi_nex_768px.py"]

# 🎬 VI-NEX-AI: ANIMACIÓN GENERAL
style_config = dict(
    style_preset="general_animation",   # Animación general
    art_style="cartoon",                # Estilo cartoon
    animation_type="2d_animation",      # Animación 2D
    color_palette="cartoon_vibrant",    # Colores vibrantes cartoon
    character_design="cartoon_style",   # Diseño cartoon
    motion_style="smooth_animation",    # Movimiento suave
    description="Animación 2D general estilo cartoon con movimientos fluidos - VI-NEX-AI"
)

# 🎪 Optimizaciones para animación general
sampling_option = dict(
    resolution="768px",
    aspect_ratio="16:9",
    num_frames=192,                     # 8 segundos @ 24fps
    fps_target=24,
    num_steps=60,                       # Pasos balanceados
    shift=True,
    temporal_reduction=3,
    is_causal_vae=True,
    guidance=7.5,                       # Guía estándar
    guidance_img=3.5,
    text_osci=True,
    image_osci=True,
    scale_temporal_osci=True,
    method="vi_nex_animation_style",
    seed=None,
    animation_smoothness=0.8,           # Suavidad de animación
    exaggeration_factor=0.6,            # Factor de exageración cartoon
)
motion_score = "4"                      # Movimiento cartoon
fps_save = 24

# 🎨 Modelo para animación general
model = dict(
    type="vi_nex_flux_animation",
    from_pretrained="./ckpts/vi_nex_ai_animation.safetensors",
    guidance_embed=True,
    fused_qkv=True,
    use_liger_rope=True,
    # Arquitectura para animación
    in_channels=64,
    vec_in_dim=1024,
    context_in_dim=5120,
    hidden_size=4096,
    mlp_ratio=4.0,
    num_heads=32,
    depth=24,
    depth_single_blocks=48,
    axes_dim=[32, 64, 64],
    theta=20_000,
    qkv_bias=True,
    cond_embed=True,
    cartoon_enhancement=True,           # Mejoras cartoon
    motion_smoothing=0.7,               # Suavizado de movimiento
    style_flexibility=0.8,              # Flexibilidad de estilo
)

save_dir = "vi_nex_samples_animation"