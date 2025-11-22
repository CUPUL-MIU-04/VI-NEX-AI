_base_ = ["../vi_nex_768px.py"]

# 🎨 VI-NEX-AI: 3D ESTILO CARTOON (Pixar/Disney)
style_config = dict(
    style_preset="3d_cartoon",          # 3D estilo cartoon
    art_style="3d_cartoon",             # Estilo Pixar/Disney
    animation_type="3d_stylized",       # Render estilizado
    rendering_quality="stylized",       # Calidad estilizada
    lighting_model="stylized_pbr",      # Iluminación PBR estilizada
    material_quality="stylized",        # Materiales estilizados
    character_design="3d_cartoon",      # Diseño de personajes 3D cartoon
    description="Animación 3D estilo cartoon tipo Pixar/Disney - VI-NEX-AI"
)

sampling_option = dict(
    resolution="768px",
    aspect_ratio="16:9", 
    num_frames=192,
    fps_target=24,
    num_steps=80,
    guidance=8.0,
    method="vi_nex_3d_cartoon",
    style_strength=0.85,               # Fuerza del estilo cartoon 3D
    cartoon_exaggeration=0.7,          # Exageración cartoon
)
motion_score = "4"

model = dict(
    type="vi_nex_flux_3d_cartoon",
    from_pretrained="./ckpts/vi_nex_ai_3d_cartoon.safetensors",
    three_d_cartoon_enhancement=True,  # Mejoras específicas para 3D cartoon
    stylized_lighting=True,            # Iluminación estilizada
    soft_shadows=True,                 # Sombras suaves
)

save_dir = "vi_nex_samples_3d_cartoon"