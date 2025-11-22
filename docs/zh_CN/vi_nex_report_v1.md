# VI-NEX-AI v1 Reporte Técnico

## Resumen de Modificaciones

VI-NEX-AI se basa en Open-Sora con las siguientes mejoras clave:

### 🚀 Arquitecturas Optimizadas
- **Modelo VI-NEX-Flux**: Arquitectura mejorada con hidden_size=4096, 32 cabezas de atención, 24 capas
- **AutoEncoder VI-NEX**: Mejor compresión espacial y temporal
- **Soporte multi-resolución**: 256px, 512px, 768px, 1024px, 2048px

### ⚡ Configuraciones de Entrenamiento
- **Learning rates optimizados**: Progresión 8e-6 → 6e-5 → 4e-5
- **Buckets mejorados**: Soporte para duraciones de 2-30 segundos
- **Parallelism VI-NEX**: Configuraciones híbridas TP/SP/PP

### 🎯 Casos de Uso Específicos
- **Videos cortos** (2-5s): `vi_nex_short_video.py`
- **Duración estándar** (4-10s): `vi_nex_standard_video.py`  
- **Videos largos** (10-30s): `vi_nex_long_video.py`

## Configuraciones Clave

### Inferencia
```bash
# Alta calidad
python inference.py --config vi_nex_1024px.py

# Videos rápidos
python inference.py --config vi_nex_short_video.py

# T2I2V premium
python inference.py --config vi_nex_t2i2v_1024px.py