# Configuración VI-NEX-AI para compresión ultra
dtype = "bf16"
batch_size = 1  # Batch pequeño para máxima compresión
seed = 42
save_dir = "vi_nex_samples/ultra_compression"

dataset = dict(
    type="video_text",
    transform_name="resize_crop", 
    fps_max=24,  # FPS estándar para compresión
    data_path="datasets/vi_nex_pexels.csv",
)

# Buckets enfocados en compresión
bucket_config = {
    "512px_ar1:1": {128: (1.0, 2)},
    "768px_ar16:9": {96: (0.8, 1)},
    "1024px_ar16:9": {64: (0.6, 1)},
}

num_workers = 16
num_bucket_build_workers = 12
prefetch_factor = 4

model = dict(
    type="vi_nex_ultra_ae",
    model_name="vi-nex-ultra-ae-f64t16c512",
    from_pretrained="./ckpts/vi_nex_ultra_ae.safetensors",
    from_scratch=True,
    use_spatial_tiling=True,
    use_temporal_tiling=True,
    spatial_tile_size=512,
    temporal_tile_size=128,  # Alta compresión temporal
    tile_overlap_factor=0.05,  # Mínimo overlap para máxima compresión
    compression_ratio=128,  # Compresión ultra
    quality_preset="ultra_compression",
    latent_channels=8,  # Menos canales para más compresión
)

plugin = "zero2"  # Plugin simple para compresión