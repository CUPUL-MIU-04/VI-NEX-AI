_base_ = ["t2i2v_768px.py"]  # Heredar de alta resolución

# Configuración premium T2I2V para VI-NEX-AI
save_dir = "vi_nex_t2i2v_1024"
sampling_option = dict(
    resolution="1024px",
    aspect_ratio="16:9", 
    num_frames=144,
    num_steps=100,           # Sampling extenso para transiciones suaves
    guidance=8.5,
    guidance_img=5.0,        # Guía de imagen fuerte
    method="vi_nex_t2i2v_premium",
    temporal_reduction=2,    # Preservar detalles temporales
)
motion_score = "6"

# Modelo Flux premium para T2I2V
img_flux = dict(
    type="vi_nex_flux_t2i2v_premium",
    from_pretrained="./ckpts/vi_nex_ai_t2i2v_1024.safetensors",
    guidance_embed=True,
    in_channels=128,
    vec_in_dim=1536,
    context_in_dim=5120,
    hidden_size=5120,
    mlp_ratio=4.0,
    num_heads=40,
    depth=28,
    axes_dim=[40, 64, 64],
    theta=25_000,
    qkv_bias=True,
    cond_embed=True,
)

img_flux_ae = dict(
    type="vi_nex_autoencoder_premium",
    from_pretrained="./ckpts/vi_nex_ae_t2i2v_premium.safetensors", 
    resolution=1024,
    in_channels=3,
    ch=256,
    out_ch=3,
    ch_mult=[1, 2, 4, 8],
    num_res_blocks=4,
    z_channels=32,
    scale_factor=0.25,
    shift_factor=0.08,
)
img_resolution = "1024px"

# Paralelismo agresivo para T2I2V de alta resolución
plugin = "vi_nex_t2i2v_premium"
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

plugin_ae = "vi_nex_hybrid"
plugin_config_ae = dict(
    tp_size=4,
    pp_size=1,
    sp_size=1,
    zero_stage=2,
    overlap_allgather=True,
)