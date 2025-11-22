_base_ = ["../vi_nex_768px.py"]

# 🎥 VI-NEX-AI: 50 FPS SUPER REALISTA - ESTÁNDAR
video_fps_config = dict(
    fps_target=50,
    quality_preset="super_realistic",
    motion_blur_simulation=True,
    temporal_consistency="ultra_high",  # Coherencia temporal ultra
    description="50 FPS para contenido estándar con realismo cinematográfico - VI-NEX-AI"
)

# ⚖️ Balance calidad-rendimiento para 50 FPS
sampling_option = dict(
    resolution="768px",
    aspect_ratio="16:9",
    num_frames=350,                     # 7 segundos @ 50fps
    fps_target=50,
    num_steps=100,                      # Máxima calidad
    shift=True,
    temporal_reduction=1,               # Mínima compresión temporal
    is_causal_vae=True,
    guidance=8.5,                       # Guía muy alta
    guidance_img=4.5,
    text_osci=False,
    image_osci=False,
    scale_temporal_osci=False,
    method="vi_nex_50fps_cinematic",
    seed=None,
)
motion_score = "5"                      # Movimiento cinematográfico
fps_save = 50

# 🎬 Modelo cinematográfico 50 FPS
model = dict(
    type="vi_nex_flux_50fps_cinematic",
    from_pretrained="./ckpts/vi_nex_ai_50fps_cinematic.safetensors",
    guidance_embed=True,
    fused_qkv=True,
    use_liger_rope=True,
    in_channels=128,
    vec_in_dim=1536,
    context_in_dim=6144,
    hidden_size=5120,
    mlp_ratio=4.0,
    num_heads=40,
    depth=28,
    depth_single_blocks=56,
    axes_dim=[40, 64, 64],
    theta=30_000,
    qkv_bias=True,
    cond_embed=True,
    temporal_attention_blocks=12,       # Más atención temporal
    use_cinematic_attention=True,       # Atención cinematográfica
)

# 💻 Configuración avanzada de memoria
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=4,
    pp_size=1,
    sp_size=16,
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
    static_graph=True,
    zero_stage=2,
    overlap_allgather=True,
)

save_dir = "vi_nex_samples_50fps_standard"