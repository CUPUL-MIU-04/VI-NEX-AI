# __init__.py
from .conditioner import HFEmbedder, VINEXAITextEmbedder

# conditioner.py (añadir después de las clases existentes)
@MODELS.register_module("vi_nex_text_embedder")
class VINEXAITextEmbedder(HFEmbedder):
    """Embedder de texto optimizado para VI-NEX-AI con capacidades extendidas"""
    
    def __init__(self, from_pretrained: str, max_length: int, shardformer: bool = False,
                 vi_nex_enhancement: bool = True, **hf_kwargs):
        super().__init__(from_pretrained, max_length, shardformer, **hf_kwargs)
        
        self.vi_nex_enhancement = vi_nex_enhancement
        if vi_nex_enhancement:
            # Parámetro de escalado para embeddings de VI-NEX-AI
            self.embedding_scale = nn.Parameter(torch.tensor(1.0))
            # Capa de normalización adicional
            self.vi_nex_norm = nn.LayerNorm(self.hf_module.config.hidden_size)
    
    def forward(self, text: list[str], added_tokens: int = 0, seq_align: int = 1,
                enhancement_factor: float = 1.0) -> Tensor:
        # Usar el forward del padre
        embeddings = super().forward(text, added_tokens, seq_align)
        
        # Aplicar mejoras de VI-NEX-AI
        if self.vi_nex_enhancement:
            embeddings = self.vi_nex_norm(embeddings)
            embeddings = embeddings * self.embedding_scale * enhancement_factor
        
        return embeddings
    
    def encode_with_attention(self, text: list[str]) -> tuple[Tensor, Tensor]:
        """Método adicional para VI-NEX-AI que devuelve embeddings y atención"""
        batch_encoding = self.tokenizer(
            text,
            truncation=True,
            max_length=self.max_length,
            return_length=False,
            return_overflowing_tokens=False,
            padding="max_length",
            return_tensors="pt",
        )
        
        outputs = self.hf_module(
            input_ids=batch_encoding["input_ids"].to(self.hf_module.device),
            attention_mask=batch_encoding["attention_mask"].to(self.hf_module.device) if "attention_mask" in batch_encoding else None,
            output_hidden_states=False,
            output_attentions=True,  # Devolver attention masks
        )
        
        embeddings = outputs[self.output_key]
        attention_mask = batch_encoding.get("attention_mask", None)
        
        return embeddings, attention_mask


class VINEXAIMultiModalTextEmbedder(nn.Module):
    """Embedder multimodal para VI-NEX-AI que combina múltiples modelos de texto"""
    
    def __init__(self, clip_model: str, t5_model: str, max_length: int = 256):
        super().__init__()
        self.clip_embedder = HFEmbedder(clip_model, max_length)
        self.t5_embedder = HFEmbedder(t5_model, max_length)
        
        # Fusionar embeddings
        self.fusion_proj = nn.Linear(
            self.clip_embedder.hf_module.config.hidden_size + 
            self.t5_embedder.hf_module.config.hidden_size,
            self.clip_embedder.hf_module.config.hidden_size  # Tamaño unificado
        )
        
    def forward(self, text: list[str]) -> Tensor:
        clip_emb = self.clip_embedder(text)
        t5_emb = self.t5_embedder(text)
        
        # Concatenar y proyectar
        combined = torch.cat([clip_emb, t5_emb], dim=-1)
        fused_emb = self.fusion_proj(combined)
        
        return fused_emb


# Mejorar la función de shardformer para VI-NEX-AI
def vi_nex_shardformer_t5(t5: T5EncoderModel, enable_tensor_parallelism: bool = True) -> T5EncoderModel:
    """
    Shardformer optimizado para VI-NEX-AI con más opciones de configuración
    """
    dtype = t5.shared.weight.dtype
    shard_config = ShardConfig(
        enable_tensor_parallelism=enable_tensor_parallelism,
        enable_jit_fused=True,
        enable_flash_attention=True,  # Habilitar flash attention si está disponible
    )
    
    shard_former = ShardFormer(shard_config=shard_config)
    optim_model, _ = shard_former.optimize(t5, policy=T5EncoderPolicy())
    optim_model = optim_model.to(dtype).eval().requires_grad_(False)
    
    return optim_model