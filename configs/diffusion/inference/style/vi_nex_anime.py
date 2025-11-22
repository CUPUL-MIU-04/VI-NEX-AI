_base_ = ["../vi_nex_768px.py"]

# 🎨 VI-NEX-AI: ESTILO ANIME JAPONÉS
style_config = dict(
    style_preset="japanese_anime",      # Estilo anime tradicional
    art_style="anime",                  # Modo anime activado
    line_emphasis="strong",             # Líneas definidas
    color_palette="vibrant_anime",      # Paleta de colores anime
    character_design="anime_style",     # Diseño de personajes anime
    description="Estilo anime japonés tradicional con líneas definidas y colores vibrantes - VI-NEX-AI"
)

# ✨ Optimizaciones específicas para anime
sampling_option = dict(
    resolution="768px",
    aspect_ratio="16:9",
    num_frames=180,                     # 7.5 segundos @ 24fps
    fps_target=24,
    num_steps=70,                       # Pasos balanceados para anime
    shift=True,
    temporal_reduction=3,
    is_causal_vae=True,
    guidance=8.5,                       # Guía alta para detalles de línea
    guidance_img=4.0,
    text_osci=True,
    image_osci=True,
    scale_temporal_osci=True,
    method="vi_nex_anime_style",
    seed=None,
    style_strength=0.8,                 # Fuerza del estilo anime
)
motion_score = "5"                      # Movimiento anime dinámico
fps_save = 24

# 🖌️ Modelo especializado en anime
model = dict(
    type="vi_nex_flux_anime",
    from_pretrained="./ckpts/vi_nex_ai_anime.safetensors",
    guidance_embed=True,
    fused_qkv=True,
    use_liger_rope=True,
    # Arquitectura optimizada para anime
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
    anime_enhancement=True,             # Mejoras específicas para anime
    line_detection_strength=0.7,        # Fuerza de detección de líneas
    color_saturation_boost=1.2,         # Boost de saturación de colores
)

# 🎭 AutoEncoder optimizado para anime
ae = dict(
    type="vi_nex_autoencoder_anime",
    from_pretrained="./ckpts/vi_nex_ae_anime.safetensors",
    in_channels=3,
    out_channels=3,
    layers_per_block=3,
    latent_channels=24,
    use_spatial_tiling=True,
    use_temporal_tiling=True,
    spatial_tile_size=512,
    temporal_tile_size=32,
    tile_overlap_factor=0.15,
    anime_compression=True,             # Compresión optimizada para anime
)

save_dir = "vi_nex_samples_anime"