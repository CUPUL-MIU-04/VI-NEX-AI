_base_ = ["../vi_nex_512px.py"]

# 🎮 VI-NEX-AI: 3D LOW POLY
style_config = dict(
    style_preset="low_poly_3d",         # 3D low poly
    art_style="low_poly",               # Estilo low poly
    animation_type="low_poly_render",   # Render low poly
    rendering_quality="low_poly",       # Calidad low poly
    polygon_count="low",                # Conteo bajo de polígonos
    description="Animación 3D estilo low poly para videojuegos y estilo retro - VI-NEX-AI"
)

sampling_option = dict(
    resolution="512px",                 # Resolución más baja para estilo
    aspect_ratio="16:9",
    num_frames=180,
    fps_target=24, 
    num_steps=50,                       # Menos pasos para estilo
    guidance=6.5,                       # Guía más baja
    method="vi_nex_3d_low_poly",
    low_poly_strength=0.9,              # Fuerza del estilo low poly
    geometric_simplification=0.8,       # Simplificación geométrica
)
motion_score = "5"                      # Movimiento más dinámico

model = dict(
    type="vi_nex_flux_3d_low_poly", 
    from_pretrained="./ckpts/vi_nex_ai_3d_low_poly.safetensors",
    low_poly_optimization=True,         # Optimizaciones low poly
    geometric_stylization=True,         # Estilización geométrica
    flat_shading=True,                  # Sombreado plano
)

save_dir = "vi_nex_samples_3d_low_poly"