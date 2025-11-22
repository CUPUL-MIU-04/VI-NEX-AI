_base_ = ["vi_nex_image.py"]

# Configuración de alta compresión para VI-NEX-AI
bucket_config = {
    "_delete_": True,
    "512px": {                  # Enfocado en 512px para compresión
        1: (1.0, 25),
        16: (1.0, 12),
        32: (1.0, 10),
        48: (1.0, 8),
        64: (1.0, 6),
        80: (1.0, 5),
        96: (1.0, 4),
        112: (1.0, 3),
        128: (1.0, 2),
    },
}

condition_config = dict(
    t2v=1,
    i2v_head=8,                 # Más peso para I2V
    i2v_tail=2,
)

grad_ckpt_settings = (100, 100)
patch_size = 1
model = dict(
    from_pretrained=None,
    grad_ckpt_settings=grad_ckpt_settings,
    in_channels=128,
    cond_embed=True,
    patch_size=patch_size,
)

# AutoEncoder de compresión profunda para VI-NEX-AI
ae = dict(
    _delete_=True,
    type="vi_nex_dc_ae",
    model_name="vi-nex-dc-ae-f32t8c256",
    from_pretrained="./ckpts/vi_nex_dc_ae.safetensors",
    from_scratch=True,
    scaling_factor=0.4,         # Factor de escalado optimizado
    use_spatial_tiling=True,
    use_temporal_tiling=True,
    spatial_tile_size=384,      # Tiles optimizados
    temporal_tile_size=48,
    tile_overlap_factor=0.2,    # Más overlap para mejor calidad
)

is_causal_vae = False
ae_spatial_compression = 32

ckpt_every = 200
lr = 2.5e-5
optim = dict(lr=lr)