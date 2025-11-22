_base_ = ["../style/vi_nex_animation.py"]

# 🎬 VI-NEX-AI: ANIMACIÓN GENERAL - 25 SEGUNDOS
video_duration_config = dict(
    max_duration_seconds=35,
    min_duration_seconds=15,
    target_duration_seconds=25,
    fps_target=20,                      # FPS reducido
    variable_length=False,
    description="Animación general de larga duración (15-35s) - VI-NEX-AI"
)

# 🎪 Optimizado para animación larga
sampling_option = dict(
    resolution="768px",
    aspect_ratio="16:9",
    num_frames=500,                     # 25 segundos @ 20fps
    fps_target=20,
    num_steps=60,                       # Pasos balanceados
    shift=True,
    temporal_reduction=2,
    is_causal_vae=True,
    guidance=6.5,                       # Guía balanceada
    guidance_img=3.0,
    text_osci=False,                    # Sin oscilación para estabilidad
    image_osci=False,
    scale_temporal_osci=False,
    method="vi_nex_animation_long",
    seed=None,
    animation_smoothness=0.7,
    exaggeration_factor=0.5,            # Exageración reducida para larga duración
)
motion_score = "3"                      # Movimiento suave
fps_save = 20

# 💾 Configuración de memoria
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=2,
    pp_size=1,
    sp_size=12,
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
    static_graph=True,
    zero_stage=2,
    overlap_allgather=True,
)

# 🎨 Modelo optimizado para animación larga
model = dict(
    type="vi_nex_flux_animation_long",
    from_pretrained="./ckpts/vi_nex_ai_animation_25s.safetensors",
    guidance_embed=True,
    fused_qkv=True,
    use_liger_rope=True,
    max_sequence_length=1536,
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
    cartoon_enhancement=True,
    long_sequence_optimization=True,    # Optimización para secuencias largas
)

save_dir = "vi_nex_samples_animation_25s"