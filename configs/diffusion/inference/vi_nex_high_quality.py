_base_ = ["256px.py"]

# Configuración de alta calidad VI-NEX-AI
save_dir = "vi_nex_hq_samples"
sampling_option = dict(
    resolution="1024px",
    aspect_ratio="16:9",
    num_frames=160,
    num_steps=120,           # Máximo sampling para calidad
    guidance=9.0,
    guidance_img=5.0,
    text_osci=True,
    image_osci=True,
    scale_temporal_osci=True,
    method="vi_nex_hq",
    temporal_reduction=2,    # Menor compresión temporal
)
motion_score = "6"
fps_save = 30

# Modelo optimizado para calidad
model = dict(
    type="vi_nex_flux_hq",
    from_pretrained="./ckpts/vi_nex_ai_hq.safetensors",
    guidance_embed=True,
    fused_qkv=True,
    use_liger_rope=True,
    in_channels=128,
    vec_in_dim=1024,
    context_in_dim=5120,
    hidden_size=5120,
    mlp_ratio=4.0,
    num_heads=40,
    depth=28,
    depth_single_blocks=56,
    axes_dim=[40, 64, 64],
    theta=25_000,
    qkv_bias=True,
    cond_embed=True,
)

# AutoEncoder de alta calidad
ae = dict(
    type="vi_nex_dc_ae",
    from_pretrained="./ckpts/vi_nex_ae_hq.safetensors",
    model_name="vi-nex-ae-f32t8c256",
    use_spatial_tiling=True,
    use_temporal_tiling=True,
    spatial_tile_size=512,
    temporal_tile_size=64,
    tile_overlap_factor=0.1,  # Menor overlap para más calidad
)

# Paralelismo optimizado para calidad
plugin = "vi_nex_quality"
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