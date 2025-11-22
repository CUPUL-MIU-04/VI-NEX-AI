_base_ = ["vi_nex_image.py"]

dataset = dict(memory_efficient=False)

# Buckets específicos para stage 1 de VI-NEX-AI
bucket_config = {
    "_delete_": True,
    "256px": {
        1: (1.0, 50),
        5: (1.0, 15),
        9: (1.0, 15),
        # ... (mantener estructura similar pero ajustar pesos)
        129: (1.0, 4),          # Más muestras para frames largos
    },
    "512px": {                  # Nueva resolución
        1: (0.8, 20),
        5: (0.8, 12),
        33: (0.8, 8),
        65: (0.8, 5),
        97: (0.8, 4),
        129: (0.8, 3),
    },
    "768px": {
        1: (0.6, 15),
        5: (0.6, 8),
        33: (0.6, 6),
    },
    "1024px": {
        1: (0.4, 10),
        5: (0.4, 6),
    },
    "2048px": {
        1: (0.2, 5),            # Resolución ultra
    },
}

model = dict(grad_ckpt_settings=(8, 100))
lr = 6e-5                      # LR más alto para stage 1
optim = dict(lr=lr)
ckpt_every = 1500
keep_n_latest = 25