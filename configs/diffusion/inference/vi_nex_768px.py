_base_ = ["768px.py"]  # Heredar de 768px original

save_dir = "vi_nex_samples_768"
sampling_option = dict(
    resolution="768px",
    num_frames=129,
    num_steps=75,           # Más pasos para mejor calidad
    guidance=8.0,           # Guía más precisa
    method="vi_nex_enhanced",
)
motion_score = "5"

model = dict(
    type="vi_nex_flux_enhanced",
    from_pretrained="./ckpts/vi_nex_ai_hq_768.safetensors",
    hidden_size=4096,
    depth=24,
    num_heads=32,
    axes_dim=[32, 56, 56],
)

# Sequence parallelism para manejar mayor resolución
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=2,
    pp_size=1,
    sp_size=4,
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
)