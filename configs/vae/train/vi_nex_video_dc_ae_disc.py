_base_ = ["vi_nex_video_dc_ae.py"]

# Configuración del discriminador para VI-NEX-AI
discriminator = dict(
    type="vi_nex_3d_discriminator",
    from_pretrained=None,
    input_nc=3,
    n_layers=6,                  # Más capas
    ndf=64,                      # Más filtros
    conv_cls="conv3d",
    use_spectral_norm=True,      # Norma espectral para estabilidad
    attention_layers=[2, 4],     # Capas de atención
)

disc_lr_scheduler = dict(
    warmup_steps=500,
    decay_type="linear",
)

# Configuraciones de pérdida del generador
gen_loss_config = dict(
    gen_start=1000,              # Inicio retardado del generador
    disc_weight=0.1,             # Peso aumentado del discriminador
    feature_matching_weight=0.5, # Coincidencia de características
)

# Configuraciones de pérdida del discriminador
disc_loss_config = dict(
    disc_start=0,
    disc_loss_type="hinge",      # Pérdida hinge para estabilidad
    gradient_penalty_weight=10.0, # Penalización de gradiente
    drift_weight=0.001,          # Peso de deriva
)

# Optimizador del discriminador
optim_discriminator = dict(
    cls="HybridAdam",
    lr=2e-4,                     # LR más alto para discriminador
    eps=1e-8,
    weight_decay=0.0,
    adamw_mode=True,
    betas=(0.5, 0.9),            # Betas ajustadas para GAN
)

grad_checkpoint = True
model = dict(
    disc_off_grad_ckpt=True,     # Checkpointing para discriminador
    use_ema=True,                # EMA para generador
    ema_decay=0.999,
)

# Ajustes de entrenamiento GAN
batch_size_ratio = 4             # Ratio de batches discriminator/generator
disc_update_freq = 1             # Frecuencia de actualización del discriminador