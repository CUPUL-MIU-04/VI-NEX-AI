_base_ = ["256px.py"]

save_dir = "vi_nex_samples_1024"
sampling_option = dict(
    resolution="1024px",
    aspect_ratio="16:9",
    num_frames=180,         # Videos más largos
    num_steps=100,          # Sampling de alta calidad
    guidance=8.5,
    guidance_img=4.0,
    method="vi_nex_premium",
)
motion_score = "6"
fps_save = 30               # FPS más suave

model = dict(
    type="vi_nex_flux_premium",
    from_pretrained="./ckpts/vi_nex_ai_premium_1024.safetensors",
    in_channels=128,
    vec_in_dim=1024,
    context_in_dim=5120,
    hidden_size=5120,
    mlp_ratio=4.0,
    num_heads=40,
    depth=28,
    axes_dim=[40, 64, 64],
    theta=20_000,
    cond_embed=True,
)

# Parallelismo agresivo para alta resolución
plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=4,
    pp_size=1,
    sp_size=8,
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
    static_graph=True,
    zero_stage=2,
    overlap_allgather=True,
)