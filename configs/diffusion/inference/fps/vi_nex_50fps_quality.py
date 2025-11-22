_base_ = ["../vi_nex_1024px.py"]

# 🎥 VI-NEX-AI: 50 FPS CALIDAD MÁXIMA
video_fps_config = dict(
    fps_target=50,
    quality_preset="ultimate_quality",  # Calidad última
    motion_blur_simulation=True,
    temporal_consistency="maximum",     # Máxima coherencia posible
    frame_interpolation=True,           # Interpolación de frames
    description="50 FPS calidad máxima para proyectos premium - VI-NEX-AI"
)

# 🏆 Configuración premium 50 FPS
sampling_option = dict(
    resolution="1024px",
    aspect_ratio="16:9",
    num_frames=250,                     # 5 segundos @ 50fps (más corto por calidad)
    fps_target=50,
    num_steps=150,                      # Sampling extenso
    shift=True,
    temporal_reduction=1,               # Sin compresión temporal
    is_causal_vae=True,
    guidance=9.0,                       # Guía máxima
    guidance_img=5.0,
    text_osci=False,
    image_osci=False,
    scale_temporal_osci=False,
    method="vi_nex_50fps_ultimate",
    seed=None,
)
motion_score = "4"                      # Movimiento controlado premium
fps_save = 50

# 💎 Modelo ultimate 50 FPS
model = dict(
    type="vi_nex_flux_50fps_ultimate",
    from_pretrained="./ckpts/vi_nex_ai_50fps_ultimate.safetensors",
    guidance_embed=True,
    fused_qkv=True,
    use_liger_rope=True,
    in_channels=192,
    vec_in_dim=2048,
    context_in_dim=8192,
    hidden_size=6144,
    mlp_ratio=4.0,
    num_heads=48,
    depth=32,
    depth_single_blocks=64,
    axes_dim=[48, 80, 80],
    theta=40_000,
    qkv_bias=True,
    cond_embed=True,
    temporal_attention_blocks=16,       # Máxima atención temporal
    use_cinematic_attention=True,
    use_frame_interpolation=True,       # Interpolación integrada
    quality_boost="ultra",              # Boost de calidad
)

# 🚀 Configuración extrema de performance
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=8,
    pp_size=2,
    sp_size=24,
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
    static_graph=True,
    zero_stage=3,                       # ZeRO stage 3
    overlap_allgather=True,
    offload_optimizer=True,
    offload_param=True,
)

save_dir = "vi_nex_samples_50fps_quality"