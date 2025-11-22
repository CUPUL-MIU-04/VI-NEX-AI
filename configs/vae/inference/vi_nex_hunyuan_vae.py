# Configuración VI-NEX-AI para Hunyuan VAE
dtype = "bf16"
batch_size = 4  # Aumentado para mejor throughput
seed = 42
save_dir = "vi_nex_samples/hunyuan_vae"

plugin = "vi_nex_zero2"
dataset = dict(
    type="video_text",
    transform_name="resize_crop",
    fps_max=30,  # Mayor FPS para VI-NEX-AI
    data_path="datasets/vi_nex_pexels.csv",  # Dataset específico
)

# Buckets optimizados para VI-NEX-AI
bucket_config = {
    "512px_ar1:1": {97: (1.0, 4)},
    "768px_ar16:9": {129: (1.0, 2)},
    "1024px_ar16:9": {180: (0.8, 1)},
    "2048px_ar16:9": {240: (0.5, 1)},
}

num_workers = 32  # Más workers para mayor velocidad
num_bucket_build_workers = 24
prefetch_factor = 8  # Prefetch aumentado

model = dict(
    type="vi_nex_hunyuan_vae",  # VAE personalizado
    from_pretrained="./ckpts/vi_nex_hunyuan_vae.safetensors",
    in_channels=3,
    out_channels=3,
    layers_per_block=3,  # Más capas para mejor calidad
    latent_channels=24,  # Más canales latentes
    scale_factor=0.38,   # Factor de escalado optimizado
    shift_factor=0.02,
    use_spatial_tiling=True,
    use_temporal_tiling=True,
    time_compression_ratio=4,
    spatial_tile_size=512,  # Tiles más grandes
    temporal_tile_size=48,  # Más frames por tile
    tile_overlap_factor=0.1,  # Overlap reducido para eficiencia
)