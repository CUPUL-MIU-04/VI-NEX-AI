_base_ = ["../style/vi_nex_animation_3d.py"]

# 🎬 VI-NEX-AI: ANIMACIÓN 3D - 25 SEGUNDOS
video_duration_config = dict(
    max_duration_seconds=35,
    min_duration_seconds=15,
    target_duration_seconds=25,
    fps_target=20,                      # FPS reducido para eficiencia
    variable_length=False,              # Longitud fija para estabilidad
    description="Animación 3D de larga duración (15-35s) - VI-NEX-AI"
)

# ⚡ Optimizado para 25 segundos de 3D
sampling_option = dict(
    resolution="768px",                 # Resolución balanceada
    aspect_ratio="16:9",
    num_frames=500,                     # 25 segundos @ 20fps
    fps_target=20,
    num_steps=80,                       # Pasos balanceados
    shift=True,
    temporal_reduction=2,               # Menor compresión temporal
    is_causal_vae=True,
    guidance=6.5,                       # Guía reducida para coherencia
    guidance_img=3.0,
    text_osci=False,                    # Sin oscilación para estabilidad
    image_osci=False,
    scale_temporal_osci=False,
    method="vi_nex_3d_long",
    seed=None,
)
motion_score = "3"                      # Movimiento conservador
fps_save = 20

# 💾 Configuración de memoria para secuencias largas
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=4,
    pp_size=1,
    sp_size=16,                         # Alto sequence parallelism
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
    static_graph=True,
    zero_stage=3,                       # ZeRO stage 3 para ahorro de memoria
    overlap_allgather=True,
)

# 🤖 Modelo optimizado para secuencias 3D largas
model = dict(
    type="vi_nex_flux_3d_long",
    from_pretrained="./ckpts/vi_nex_ai_3d_25s.safetensors",
    guidance_embed=True,
    fused_qkv=True,
    use_liger_rope=True,
    max_sequence_length=1536,           # Secuencia muy larga
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
    three_d_enhancement=True,
    temporal_consistency_boost=True,    # Boost de coherencia temporal
)

save_dir = "vi_nex_samples_3d_25s"