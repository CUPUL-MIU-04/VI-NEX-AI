_base_ = ["../style/vi_nex_animation_3d.py"]

# 🎬 VI-NEX-AI: SUPER REALISTA - 25 SEGUNDOS
video_duration_config = dict(
    max_duration_seconds=35,
    min_duration_seconds=15,
    target_duration_seconds=25,
    fps_target=18,                      # FPS muy reducido para máxima calidad
    variable_length=False,
    description="Contenido super realista de larga duración (15-35s) - VI-NEX-AI"
)

# 🌟 Optimizado para realismo máximo en larga duración
sampling_option = dict(
    resolution="768px",                 # Resolución balanceada
    aspect_ratio="16:9",
    num_frames=450,                     # 25 segundos @ 18fps
    fps_target=18,
    num_steps=100,                      # Máxima calidad
    shift=True,
    temporal_reduction=1,               # Mínima compresión temporal
    is_causal_vae=True,
    guidance=7.5,                       # Guía alta para detalles
    guidance_img=4.0,
    text_osci=False,
    image_osci=False,
    scale_temporal_osci=False,
    method="vi_nex_hyper_real_long",
    seed=None,
    photorealism_strength=0.9,
    detail_preservation=0.95,
)
motion_score = "2"                      # Movimiento muy natural
fps_save = 18

# 💻 Configuración extrema de memoria
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=4,
    pp_size=2,
    sp_size=20,                         // Documentación continua en la siguiente respuesta debido a límites de longitud
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
    static_graph=True,
    zero_stage=3,
    overlap_allgather=True,
    offload_optimizer=True,
    offload_param=True,
)

// 🤖 Modelo ultra optimizado para realismo largo
model = dict(
    type="vi_nex_flux_hyper_real_long",
    from_pretrained="./ckpts/vi_nex_ai_hyper_real_25s.safetensors",
    guidance_embed=True,
    fused_qkv=True,
    use_liger_rope=True,
    max_sequence_length=2048,           // Secuencia ultra larga
    in_channels=128,
    vec_in_dim=1536,
    context_in_dim=6144,
    hidden_size=5120,
    mlp_ratio=4.0,
    num_heads=40,
    depth=28,
    depth_single_blocks=56,
    axes_dim=[40, 64, 64],
    theta=25_000,
    qkv_bias=True,
    cond_embed=True,
    hyper_realistic_enhancement=True,
    advanced_lighting=True,
    global_illumination=True,
    temporal_consistency_max=True,      // Máxima coherencia temporal
)

save_dir = "vi_nex_samples_hyper_real_25s"