_base_ = ["../vi_nex_512px.py"]

# 🎥 VI-NEX-AI: 50 FPS SUPER REALISTA - CORTO
video_fps_config = dict(
    fps_target=50,                      # 🚀 FPS ultra altos
    quality_preset="super_realistic",   # Modo realismo máximo
    motion_blur_simulation=True,        # Simulación de motion blur
    temporal_consistency="high",        # Máxima coherencia temporal
    description="50 FPS ultra fluidos para contenido corto super realista - VI-NEX-AI"
)

# ⚡ Optimizado para 50 FPS
sampling_option = dict(
    resolution="512px",
    aspect_ratio="16:9",
    num_frames=150,                     # 3 segundos @ 50fps
    fps_target=50,                      # 🎯 50 FPS
    num_steps=80,                       # Más pasos para calidad
    shift=True,
    temporal_reduction=2,               # Menor compresión temporal
    is_causal_vae=True,
    guidance=8.0,                       # Guía alta para detalles
    guidance_img=4.0,
    text_osci=False,                    # Sin oscilación para estabilidad
    image_osci=False,
    scale_temporal_osci=False,
    method="vi_nex_50fps_enhanced",
    seed=None,
)
motion_score = "6"                      # Movimiento más dinámico
fps_save = 50                           # Exportar a 50 FPS

# 🤖 Modelo especializado para alta frecuencia temporal
model = dict(
    type="vi_nex_flux_50fps",
    from_pretrained="./ckpts/vi_nex_ai_50fps.safetensors",
    guidance_embed=True,
    fused_qkv=True,
    use_liger_rope=True,
    # Arquitectura optimizada para temporal
    in_channels=64,
    vec_in_dim=1024,
    context_in_dim=5120,
    hidden_size=4096,
    mlp_ratio=4.0,
    num_heads=32,
    depth=24,
    depth_single_blocks=48,
    axes_dim=[32, 64, 64],
    theta=25_000,
    qkv_bias=True,
    cond_embed=True,
    temporal_attention_blocks=8,        # Bloques extra de atención temporal
)

# 💾 Parallelismo para alta carga temporal
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=2,
    pp_size=1,
    sp_size=12,                         # Alto sequence parallelism
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
    static_graph=True,
    zero_stage=2,
    overlap_allgather=True,
)

save_dir = "vi_nex_samples_50fps_short"