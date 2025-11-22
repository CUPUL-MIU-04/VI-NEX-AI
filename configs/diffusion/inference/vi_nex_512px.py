_base_ = ["256px.py"]

save_dir = "vi_nex_samples_512"
sampling_option = dict(
    resolution="512px",
    aspect_ratio="16:9",
    num_frames=96,          # Duración media
    num_steps=50,           # Sampling balanceado
    guidance=7.0,
    method="vi_nex_balanced",
)
motion_score = "4"

model = dict(
    type="vi_nex_flux",
    from_pretrained="./ckpts/vi_nex_ai_balanced_512.safetensors",
    hidden_size=3072,
    depth=20,
    axes_dim=[24, 48, 48],  # Dimensión intermedia
)

# Paralelismo mínimo
plugin = "hybrid"
plugin_config = dict(
    tp_size=2,
    pp_size=1,
    sp_size=1,
    zero_stage=2,
)