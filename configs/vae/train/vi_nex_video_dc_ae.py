# ============
# VI-NEX-AI Model Config 
# ============
model = dict(
    type="vi_nex_dc_ae",
    model_name="vi-nex-dc-ae-f32t8c256",
    from_scratch=True,
    from_pretrained=None,
    latent_channels=32,           # Más canales latentes
    compression_ratio=64,         # Ratio de compresión optimizado
    use_attention=True,           # Atención incorporada
    residual_blocks=4,            # Más bloques residuales
)

# ============
# VI-NEX-AI Data Config 
# ============
dataset = dict(
    type="video_text",
    transform_name="resize_crop",
    data_path="datasets/vi_nex_pexels.csv",  # Dataset específico
    fps_max=30,                  # Mayor FPS para VI-NEX-AI
    vmaf=True,                   # Métricas de calidad
)

# Buckets optimizados para múltiples resoluciones
bucket_config = {
    "256px_ar1:1": {32: (1.0, 8)},
    "512px_ar1:1": {64: (0.8, 6)},
    "768px_ar16:9": {96: (0.6, 4)},
    "1024px_ar16:9": {128: (0.4, 2)},
}

num_bucket_build_workers = 72    # Más workers para buckets
num_workers = 16                 # Workers aumentados
prefetch_factor = 4              # Prefetch mejorado

# ============
# VI-NEX-AI Train Config 
# ============
optim = dict(
    cls="HybridAdam",
    lr=8e-5,                     # Learning rate optimizado
    eps=1e-8,
    weight_decay=0.01,           # Regularización añadida
    adamw_mode=True,
    betas=(0.9, 0.95),           # Betas ajustadas
)

lr_scheduler = dict(
    warmup_steps=1000,           # Warmup específico
    decay_type="cosine",         # Decaimiento cosine
)

mixed_strategy = "mixed_video_image"
mixed_image_ratio = 0.25         # Ratio ajustado

dtype = "bf16"
plugin = "vi_nex_zero2"
plugin_config = dict(
    reduce_bucket_size_in_m=256,  # Buckets más grandes
    overlap_allgather=True,       # Overlap activado
)

grad_clip = 1.0
grad_checkpoint = True           # Checkpointing activado
pin_memory_cache_pre_alloc_numels = [80 * 1024 * 1024] * num_workers * prefetch_factor

seed = 42
outputs = "vi_nex_outputs"
epochs = 120                     # Más épocas
log_every = 5                    # Log más frecuente
ckpt_every = 2000                # Checkpoints más frecuentes
keep_n_latest = 30               # Más checkpoints guardados
ema_decay = 0.995                # EMA más agresivo
wandb_project = "vi_nex_dcae"

update_warmup_steps = True

# ============
# VI-NEX-AI Loss Config 
# ============
vae_loss_config = dict(
    perceptual_loss_weight=0.7,  # Más peso a pérdida perceptual
    kl_loss_weight=0.001,        # KL ligero para regularización
    mse_loss_weight=1.0,
    lpips_loss_weight=0.3,       # Pérdida LPIPS añadida
    gaussian_loss=True,          # Pérdida gaussiana
)