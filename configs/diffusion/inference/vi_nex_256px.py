_base_ = ["256px.py"]  # Heredar configuración base

# Optimizaciones específicas de VI-NEX-AI
save_dir = "vi_nex_samples_256"
sampling_option = dict(
    resolution="256px",
    num_frames=64,          # Menos frames para mayor velocidad
    num_steps=30,           # Menos pasos de sampling
    guidance=6.0,           # Guía balanceada
    method="vi_nex_fast",   # Método optimizado
)

model = dict(
    type="vi_nex_flux_fast",
    from_pretrained="./ckpts/vi_nex_ai_fast_256.safetensors",
    hidden_size=2048,       # Modelo más eficiente
    depth=16,
)

# Sin paralelismo para máxima velocidad
plugin = None
plugin_config = None