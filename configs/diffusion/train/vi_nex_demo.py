_base_ = ["vi_nex_stage1.py"]

# Configuración liviana para demostraciones
bucket_config = {
    "_delete_": True,
    "512px": {                  # Enfocado en 512px para demos
        1: (1.0, 2),
        33: (1.0, 2),
        65: (1.0, 1),
        97: (1.0, 1),
        129: (1.0, 1),
    },
}

# Modelo más rápido para demostraciones
model = dict(
    grad_ckpt_settings=(4, 50), # Menos checkpointing
    hidden_size=3072,           # Modelo más pequeño
    depth=16,
)

lr = 1e-5
optim = dict(lr=lr)
ckpt_every = 500