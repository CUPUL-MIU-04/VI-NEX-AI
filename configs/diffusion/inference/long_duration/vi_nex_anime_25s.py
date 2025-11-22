_base_ = ["../style/vi_nex_anime.py"]

# 🎨 VI-NEX-AI: ANIME - 25 SEGUNDOS
video_duration_config = dict(
    max_duration_seconds=35,
    min_duration_seconds=15,
    target_duration_seconds=25,
    fps_target=20,                      # FPS reducido
    variable_length=False,
    description="Anime de larga duración (15-35s) - VI-NEX-AI"
)

# ✨ Optimizado para anime largo
sampling_option = dict(
    resolution="768px",
    aspect_ratio="16:9",
    num_frames=500,                     # 25 segundos @ 20fps
    fps_target=20,
    num_steps=70,                       # Pasos balanceados
    shift=True,
    temporal_reduction=2,
    is_causal_vae=True,
    guidance=7.0,                       # Guía balanceada
    guidance_img=3.5,
    text_osci=False,                    # Sin oscilación para estabilidad
    image_osci=False,
    scale_temporal_osci=False,
    method="vi_nex_anime_long",
    seed=None,
    style_strength=0.8,
)
motion_score = "4"                      # Movimiento anime consistente
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

# 🖌️ Modelo optimizado para anime largo
model = dict(
    type="vi_nex_flux_anime_long",
    from_pretrained="./ckpts/vi_nex_ai_anime_25s.safetensors",
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
    anime_enhancement=True,
    temporal_coherence_anime=True,      # Coherencia temporal para anime
)

save_dir = "vi_nex_samples_anime_25s"