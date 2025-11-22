_base_ = ["./vi_nex_stage1.py"]

# Configuración Image-to-Video para Stage 1 de VI-NEX-AI
model = dict(cond_embed=True)

condition_config = dict(
    t2v=1,
    i2v_head=6,  # Mayor peso para I2V en VI-NEX-AI
    i2v_loop=2,  # Conexión de imágenes con más peso
    i2v_tail=2,  # Imagen como último frame
)

# Ajustes de aprendizaje para I2V
lr = 8e-6
optim = dict(lr=lr)

# Buckets optimizados para I2V
bucket_config = {
    "_delete_": True,
    "512px": {  # Enfocado en 512px para I2V
        1: (1.0, 40),
        5: (1.0, 15),
        9: (1.0, 15),
        13: (1.0, 15),
        17: (1.0, 15),
        21: (1.0, 15),
        25: (1.0, 15),
        29: (1.0, 15),
        33: (1.0, 12),
        37: (1.0, 10),
        41: (1.0, 10),
        45: (1.0, 10),
        49: (1.0, 10),
        53: (1.0, 10),
        57: (1.0, 10),
        61: (1.0, 10),
        65: (1.0, 8),
        69: (1.0, 6),
        73: (1.0, 6),
        77: (1.0, 6),
        81: (1.0, 6),
        85: (1.0, 6),
        89: (1.0, 6),
        93: (1.0, 6),
        97: (1.0, 6),
        101: (1.0, 4),
        105: (1.0, 4),
        109: (1.0, 4),
        113: (1.0, 4),
        117: (1.0, 4),
        121: (1.0, 4),
        125: (1.0, 4),
        129: (1.0, 4),
    },
    "768px": {
        1: (0.6, 20),
        5: (0.6, 8),
        33: (0.6, 6),
    },
}