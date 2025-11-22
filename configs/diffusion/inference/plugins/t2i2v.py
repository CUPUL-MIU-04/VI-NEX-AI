use_t2i2v = True

# Configuración Flux optimizada para VI-NEX-AI
img_flux = dict(
    type="vi_nex_flux",
    from_pretrained="./ckpts/vi_nex_flux.safetensors",
    guidance_embed=True,
    # Arquitectura optimizada
    in_channels=64,
    vec_in_dim=1024,              # Aumentado para VI-NEX-AI
    context_in_dim=5120,
    hidden_size=4096,
    mlp_ratio=4.0,
    num_heads=32,
    depth=24,
    depth_single_blocks=48,
    axes_dim=[32, 64, 64],        # Mejor resolución espacial
    theta=20_000,
    qkv_bias=True,
    cond_embed=True,              # Activado para VI-NEX-AI
    vi_nex_attention=True,        # Mecanismo de atención personalizado
)

img_flux_ae = dict(
    type="vi_nex_autoencoder",
    from_pretrained="./ckpts/vi_nex_ae.safetensors",
    resolution=512,               # Mayor resolución base
    in_channels=3,
    ch=256,                       # Más canales
    out_ch=3,
    ch_mult=[1, 2, 4, 8],        # Mayor capacidad
    num_res_blocks=4,
    z_channels=32,
    scale_factor=0.3,
    shift_factor=0.1,
)
img_resolution = "1024px"         # Mayor resolución para VI-NEX-AI