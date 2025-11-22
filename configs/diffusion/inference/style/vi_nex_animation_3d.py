_base_ = ["../vi_nex_1024px.py"]

# 🎬 VI-NEX-AI: ANIMACIÓN 3D/CGI
style_config = dict(
    style_preset="3d_animation",        # Animación 3D
    art_style="cgi",                    # Estilo CGI
    animation_type="3d_render",         # Render 3D
    rendering_quality="high",           # Calidad de render alta
    lighting_model="physically_based",  # Iluminación física
    material_quality="high",            # Calidad de materiales
    description="Animación 3D/CGI con iluminación física y materiales realistas - VI-NEX-AI"
)

# 💻 Optimizaciones para 3D
sampling_option = dict(
    resolution="1024px",
    aspect_ratio="16:9",
    num_frames=180,                     # 7.5 segundos @ 24fps
    fps_target=24,
    num_steps=90,                       # Más pasos para detalles 3D
    shift=True,
    temporal_reduction=2,               # Menor compresión
    is_causal_vae=True,
    guidance=8.5,                       # Guía alta para detalles 3D
    guidance_img=4.5,
    text_osci=False,                    # Sin oscilación para estabilidad
    image_osci=False,
    scale_temporal_osci=False,
    method="vi_nex_3d_animation",
    seed=None,
    three_d_quality=0.9,                # Calidad 3D
    lighting_accuracy=0.8,              # Precisión de iluminación
)
motion_score = "5"                      # Movimiento 3D suave
fps_save = 24

# 🖥️ Modelo especializado en 3D
model = dict(
    type="vi_nex_flux_3d",
    from_pretrained="./ckpts/vi_nex_ai_3d_animation.safetensors",
    guidance_embed=True,
    fused_qkv=True,
    use_liger_rope=True,
    # Arquitectura para 3D
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
    three_d_enhancement=True,           # Mejoras 3D
    lighting_processing=True,           # Procesamiento de iluminación
    material_processing=True,           # Procesamiento de materiales
    shadow_quality="high",              # Calidad de sombras
    reflection_processing=True,         # Procesamiento de reflejos
)

# 🎮 Configuración de plugin para 3D
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=4,
    pp_size=1,
    sp_size=8,
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
    static_graph=True,
    zero_stage=2,
    overlap_allgather=True,
)

save_dir = "vi_nex_samples_animation_3d"