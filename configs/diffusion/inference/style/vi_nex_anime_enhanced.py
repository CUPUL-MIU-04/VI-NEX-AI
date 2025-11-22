_base_ = ["../vi_nex_1024px.py"]

# 🎨 VI-NEX-AI: ANIME MEJORADO - ALTA CALIDAD
style_config = dict(
    style_preset="high_quality_anime",  # Anime de alta calidad
    art_style="anime_pro",              # Modo anime profesional
    line_emphasis="ultra_strong",       # Líneas ultra definidas
    color_palette="cinematic_anime",    # Paleta cinematográfica
    character_design="detailed_anime",  # Diseño detallado
    background_quality="anime_movie",   # Calidad de fondo de película
    description="Anime de calidad cinematográfica con detalles mejorados y colores ricos - VI-NEX-AI"
)

# 🌟 Optimizaciones premium para anime
sampling_option = dict(
    resolution="1024px",
    aspect_ratio="16:9",
    num_frames=240,                     # 10 segundos @ 24fps
    fps_target=24,
    num_steps=100,                      # Máxima calidad para detalles
    shift=True,
    temporal_reduction=2,               # Menor compresión para detalles
    is_causal_vae=True,
    guidance=9.0,                       # Guía muy alta
    guidance_img=5.0,
    text_osci=False,                    # Sin oscilación para estabilidad
    image_osci=False,
    scale_temporal_osci=False,
    method="vi_nex_anime_premium",
    seed=None,
    style_strength=0.9,                 # Máxima fuerza de estilo
    detail_enhancement=1.0,             # Mejora de detalles máxima
)
motion_score = "6"                      # Movimiento cinematográfico
fps_save = 24

# 💎 Modelo premium para anime
model = dict(
    type="vi_nex_flux_anime_premium",
    from_pretrained="./ckpts/vi_nex_ai_anime_premium.safetensors",
    guidance_embed=True,
    fused_qkv=True,
    use_liger_rope=True,
    # Arquitectura premium para anime
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
    anime_enhancement=True,
    line_detection_strength=0.9,        # Detección de líneas máxima
    color_saturation_boost=1.3,         # Saturación mejorada
    shadow_enhancement=True,            # Mejora de sombras
    highlight_processing=True,          # Procesamiento de brillos
)

# 🖼️ AutoEncoder de alta calidad para anime
ae = dict(
    type="vi_nex_autoencoder_anime_hd",
    from_pretrained="./ckpts/vi_nex_ae_anime_hd.safetensors",
    in_channels=3,
    out_channels=3,
    layers_per_block=4,
    latent_channels=32,
    use_spatial_tiling=True,
    use_temporal_tiling=True,
    spatial_tile_size=768,
    temporal_tile_size=48,
    tile_overlap_factor=0.1,
    anime_compression=True,
    detail_preservation="high",         # Preservación de detalles alta
)

save_dir = "vi_nex_samples_anime_enhanced"