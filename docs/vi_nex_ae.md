# VI-NEX-AI Video AutoEncoder

VI-NEX-AI enhances video compression with improved architectures and training strategies.

## Enhanced Architectures

### VI-NEX-DC-AE
```python
model = dict(
    type="vi_nex_dc_ae",
    model_name="vi-nex-dc-ae-f32t8c256",
    latent_channels=32,
    compression_ratio=64,
    use_attention=True,
    residual_blocks=4,
)