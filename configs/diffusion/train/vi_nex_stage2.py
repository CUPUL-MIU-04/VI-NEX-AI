_base_ = ["vi_nex_image.py"]

# Configuración avanzada con parallelism
grad_ckpt_settings = (100, 100)

plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=2,
    pp_size=1,
    sp_size=8,                  # Más sequence parallelism
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
    static_graph=True,
    zero_stage=2,
    overlap_allgather=True,
)

# Buckets más agresivos para stage 2
bucket_config = {
    "_delete_": True,
    "256px": {
        1: (1.0, 150),          # Más batches para frames cortos
        5: (1.0, 20),
        # ... (estructura similar con pesos aumentados)
        129: (1.0, 8),
    },
    "512px": {
        1: (0.8, 60),
        5: (0.8, 15),
        33: (0.8, 12),
        65: (0.8, 8),
        97: (0.8, 6),
        129: (0.8, 5),
    },
    "768px": {
        1: (0.6, 45),
        5: (0.6, 12),
        33: (0.6, 10),
        65: (0.6, 7),
        97: (0.6, 5),
        129: (0.6, 4),
    },
    "1024px": {
        1: (0.4, 25),
        5: (0.4, 8),
        33: (0.4, 6),
        65: (0.4, 4),
    },
}

model = dict(
    grad_ckpt_settings=grad_ckpt_settings,
    cond_embed=True,            # Embeddings condicionales activados
)
lr = 4e-5
optim = dict(lr=lr)
ckpt_every = 150
keep_n_latest = 15