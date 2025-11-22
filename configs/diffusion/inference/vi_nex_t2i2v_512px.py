_base_ = ["t2i2v_256px.py"]  # Heredar configuración T2I2V

# Ajustes específicos para VI-NEX-AI 512px
save_dir = "vi_nex_t2i2v_512"
sampling_option = dict(
    resolution="512px",
    aspect_ratio="16:9",
    num_frames=96,
    num_steps=60,            # Más pasos para mejor transición imagen-video
    guidance=7.5,
    guidance_img=4.0,        # Guía de imagen más fuerte para T2I2V
    method="vi_nex_t2i2v",
)

# Modelo Flux optimizado para T2I2V
img_flux = dict(
    type="vi_nex_flux_t2i2v",
    from_pretrained="./ckpts/vi_nex_ai_t2i2v_512.safetensors",
    guidance_embed=True,
    in_channels=64,
    vec_in_dim=1024,
    context_in_dim=4096,
    hidden_size=3072,
    mlp_ratio=4.0,
    num_heads=24,
    depth=20,
    axes_dim=[24, 48, 48],
    theta=15_000,
    qkv_bias=True,
    cond_embed=True,         # Importante para T2I2V
)

img_flux_ae = dict(
    type="vi_nex_autoencoder",
    from_pretrained="./ckpts/vi_nex_ae_t2i2v.safetensors",
    resolution=512,
    in_channels=3,
    ch=192,
    out_ch=3,
    ch_mult=[1, 2, 4, 6],
    num_res_blocks=3,
    z_channels=24,
    scale_factor=0.3,
    shift_factor=0.1,
)

# Plugin optimizado para T2I2V
plugin = "vi_nex_t2i2v"
plugin_config = dict(
    tp_size=2,
    pp_size=1,
    sp_size=4,
    zero_stage=2,
    overlap_allgather=True,
)