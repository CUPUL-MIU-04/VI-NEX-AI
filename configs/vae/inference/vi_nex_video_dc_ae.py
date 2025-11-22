# Configuración VI-NEX-AI para DC-AE
dtype = "bf16"
batch_size = 2  # Batch balanceado para compresión
seed = 42
save_dir = "vi_nex_samples/video_dc_ae"

dataset = dict(
    type="video_text", 
    transform_name="resize_crop",
    fps_max=30,  # FPS aumentado
    data_path="datasets/vi_nex_pexels.csv",
)

# Buckets para múltiples resoluciones
bucket_config = {
    "512px_ar1:1": {96: (1.0, 4)},
    "768px_ar16:9": {128: (0.8, 2)},
    "1024px_ar16:9": {160: (0.6, 1)},
    "2048px_ar16:9": {200: (0.4, 1)},
}

num_workers = 28
num_bucket_build_workers = 20
prefetch_factor = 6

model = dict(
    type="vi_nex_dc_ae",  # DC-AE personalizado
    model_name="vi-nex-dc-ae-f32t8c256",  # Modelo mejorado
    from_pretrained="./ckpts/vi_nex_dc_ae_enhanced.safetensors",
    from_scratch=True,
    use_spatial_tiling=True,
    use_temporal_tiling=True,
    spatial_tile_size=384,  # Tiles optimizados
    temporal_tile_size=64,  # Más compresión temporal
    tile_overlap_factor=0.15,  # Overlap balanceado
    compression_ratio=64,  # Mayor compresión
    quality_preset="high",  # Preset de calidad
)

# Configuración de plugin optimizada
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=2,
    pp_size=1, 
    sp_size=1,
    zero_stage=1,
    overlap_allgather=True,
)