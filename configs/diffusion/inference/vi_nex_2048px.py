_base_ = ["256px.py"]

save_dir = "vi_nex_samples_2048"
sampling_option = dict(
    resolution="2048px",
    aspect_ratio="16:9",
    num_frames=240,         # Videos largos en ultra calidad
    num_steps=150,          # Sampling máximo
    guidance=9.0,
    guidance_img=5.0,
    method="vi_nex_ultra",
    temporal_reduction=2,   # Menor compresión temporal
)
motion_score = "7"
fps_save = 30

model = dict(
    type="vi_nex_flux_ultra",
    from_pretrained="./ckpts/vi_nex_ai_ultra_2048.safetensors",
    in_channels=192,
    vec_in_dim=1536,
    context_in_dim=6144,
    hidden_size=6144,
    mlp_ratio=4.0,
    num_heads=48,
    depth=32,
    depth_single_blocks=64,
    axes_dim=[64, 80, 80],
    theta=30_000,
    qkv_bias=True,
    cond_embed=True,
)

# Máximo paralelismo para resoluciones ultra
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=8,
    pp_size=2,
    sp_size=16,
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
    static_graph=True,
    zero_stage=3,           # ZeRO stage 3 para máxima optimización
    overlap_allgather=True,
)