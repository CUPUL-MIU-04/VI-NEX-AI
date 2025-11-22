plugin = "vi_nex_hybrid"
plugin_config = dict(
    tp_size=4,                    # Ajustado para clusters medianos
    pp_size=2,                    # Pipeline parallelism activado
    sp_size=2,                    # Sequence parallelism balanceado
    zero_stage=2,
    overlap_allgather=True,
    vi_nex_optimized=True,
)

plugin_ae = "vi_nex_hybrid"
plugin_config_ae = dict(
    tp_size=4,
    pp_size=1,
    sp_size=1,
    zero_stage=2,
    overlap_allgather=True,
)