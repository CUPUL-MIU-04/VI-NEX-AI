plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=2,                    # Ajustar según hardware disponible
    pp_size=1,
    sp_size=4,                    # Reducir para mejor estabilidad
    sequence_parallelism_mode="ring_attn_optimized",
    enable_sequence_parallelism=True,
    static_graph=True,
    zero_stage=2,
    overlap_allgather=True,       # Activar para mejor rendimiento
    vi_nex_optimized=True,        # Flag específico de VI-NEX-AI
)

plugin_ae = "vi_nex_hybrid"
plugin_config_ae = dict(
    tp_size=4,                    # Ajustado para VI-NEX-AI
    pp_size=1,
    sp_size=1,
    zero_stage=2,
    overlap_allgather=True,
)