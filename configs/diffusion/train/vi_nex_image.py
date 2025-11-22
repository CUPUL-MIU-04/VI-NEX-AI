_base_ = ["image.py"]

# Configuración base optimizada para VI-NEX-AI
dataset = dict(
    type="video_text",
    transform_name="resize_crop",
    fps_max=30,  # Mayor FPS para mejor fluidez
    vmaf=True,
)

# Buckets optimizados para VI-NEX-AI
bucket_config = {
    "256px": {1: (1.0, 60)},
    "512px": {1: (0.8, 25)},   # Nueva resolución
    "768px": {1: (0.6, 15)},
    "1024px": {1: (0.4, 10)},  # Mayor peso para alta resolución
    "2048px": {1: (0.2, 5)},   # Nueva resolución ultra
}

# Modelo VI-NEX-AI optimizado
model = dict(
    type="vi_nex_flux",
    from_pretrained=None,
    strict_load=False,
    guidance_embed=True,        # Embeddings de guía activados
    fused_qkv=True,             # QKV fusionado para eficiencia
    use_liger_rope=True,
    grad_ckpt_settings=(8, 100),
    # Arquitectura mejorada
    in_channels=128,            # Más canales de entrada
    vec_in_dim=1024,            # Dimensión aumentada
    context_in_dim=5120,        # Contexto expandido
    hidden_size=4096,           # Modelo más grande
    mlp_ratio=4.0,
    num_heads=32,               # Más cabezas de atención
    depth=24,                   # Más profundidad
    depth_single_blocks=48,
    axes_dim=[32, 64, 64],      # Mejor representación espacial
    theta=20_000,               # RoPE mejorado
    qkv_bias=True,
)

# AutoEncoder mejorado para VI-NEX-AI
ae = dict(
    type="vi_nex_autoencoder",
    from_pretrained="./ckpts/vi_nex_ae_base.safetensors",
    in_channels=3,
    out_channels=3,
    layers_per_block=3,         # Más capas
    latent_channels=24,         # Más canales latentes
    use_spatial_tiling=True,
    use_temporal_tiling=True,   # Tiling temporal activado
    spatial_tile_size=512,
    temporal_tile_size=32,
    tile_overlap_factor=0.15,   # Overlap optimizado
)

# Optimización mejorada
lr = 8e-6                      # Learning rate ajustado
optim = dict(
    cls="HybridAdam",
    lr=lr,
    eps=1e-15,
    weight_decay=0.01,          # Regularización ligera
    adamw_mode=True,
)

# Aceleración mejorada
num_workers = 16
plugin = "vi_nex_zero2"
plugin_config = dict(
    reduce_bucket_size_in_m=256,  # Buckets más grandes
    overlap_allgather=True,       # Overlap activado
)

outputs = "vi_nex_outputs"
wandb_project = "vi_nex_ai"