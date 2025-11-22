_base_ = ["vi_nex_video_dc_ae.py"]

# Configuración para entrenar Hunyuan VAE en VI-NEX-AI
model = dict(
    type="vi_nex_hunyuan_vae",
    from_scratch=True,
    from_pretrained=None,
    in_channels=3,
    out_channels=3,
    layers_per_block=3,          # Más capas
    latent_channels=24,          # Más canales latentes
    down_block_types=["DownEncoderBlock3D"] * 4,
    up_block_types=["UpDecoderBlock3D"] * 4,
    block_out_channels=[128, 256, 512, 512],
)

# Buckets específicos para Hunyuan VAE
bucket_config = {
    "256px_ar1:1": {32: (1.0, 12)},
    "512px_ar1:1": {64: (0.8, 8)},
    "768px_ar16:9": {96: (0.6, 6)},
    "1024px_ar16:9": {128: (0.4, 4)},
}

# Optimización específica para VAE
optim = dict(
    cls="HybridAdam",
    lr=1e-4,
    eps=1e-8,
    weight_decay=0.01,
    adamw_mode=True,
    betas=(0.9, 0.99),
)

vae_loss_config = dict(
    perceptual_loss_weight=0.3,
    kl_loss_weight=0.0001,       # KL muy ligero
    mse_loss_weight=1.0,
    reconstruction_loss_type="l1", # Pérdida L1 para mejores bordes
)

# Configuración de plugin optimizada
plugin = "vi_nex_zero2"
plugin_config = dict(
    reduce_bucket_size_in_m=192,
    overlap_allgather=True,
)