from copy import deepcopy
from typing import Dict, List, Optional, Union

import torch.nn as nn
from mmengine.registry import Registry


def build_module(module: dict | nn.Module, builder: Registry, **kwargs) -> nn.Module | None:
    """Build module from config or return the module itself.

    Args:
        module (dict | nn.Module): The module to build.
        builder (Registry): The registry to build module.
        *args, **kwargs: Arguments passed to build function.

    Returns:
        (None | nn.Module): The created model.
    """
    if module is None:
        return None
    if isinstance(module, dict):
        cfg = deepcopy(module)
        for k, v in kwargs.items():
            cfg[k] = v
        return builder.build(cfg)
    elif isinstance(module, nn.Module):
        return module
    elif module is None:
        return None
    else:
        raise TypeError(f"Only support dict and nn.Module, but got {type(module)}.")


MODELS = Registry(
    "model",
    locations=["opensora.models"],
)

DATASETS = Registry(
    "dataset",
    locations=["opensora.datasets"],
)

# Registros específicos para VI-NEX-AI
VAES = Registry(
    "vae", 
    locations=["opensora.models.vae", "opensora.models.dc_ae", "opensora.models.hunyuan_vae"]
)

SCHEDULERS = Registry(
    "scheduler",
    locations=["opensora.models.schedulers"]  # Nota: Verificar si este directorio existe
)

OPTIMIZERS = Registry(
    "optimizer",
    locations=["opensora.utils.optimizer"]
)

# Registro para componentes de inferencia de VI-NEX-AI
INFERENCE_MODULES = Registry(
    "inference",
    locations=["opensora.utils.inference"]
)


def register_vi_nex_ai_components():
    """Registrar componentes específicos de VI-NEX-AI"""
    # Esta función puede ser usada para registro automático de componentes personalizados
    # Por ejemplo, al importar módulos específicos de VI-NEX-AI
    try:
        # Ejemplo: Registrar componentes personalizados si existen
        from opensora.models.vi_nex_ai import custom_components
        custom_components.register()
    except ImportError:
        # Si no existen componentes personalizados, no hacer nada
        pass


def list_registered_components(registry_name: str) -> List[str]:
    """Listar todos los componentes registrados"""
    registries = {
        "models": MODELS,
        "datasets": DATASETS,
        "vaes": VAES,
        "schedulers": SCHEDULERS,
        "optimizers": OPTIMIZERS,
        "inference": INFERENCE_MODULES
    }
    
    if registry_name in registries:
        registry = registries[registry_name]
        return sorted(list(registry.module_dict.keys()))
    else:
        available = list(registries.keys())
        raise ValueError(f"Registry '{registry_name}' not found. Available: {available}")


def build_module_with_vi_nex_ai_preset(module: dict | nn.Module, builder: Registry, 
                                     preset: str = None, **kwargs) -> nn.Module | None:
    """
    Versión extendida con presets de VI-NEX-AI
    """
    if preset and isinstance(module, dict):
        # Aplicar configuraciones predefinidas de VI-NEX-AI
        vi_nex_presets = {
            "high_quality": {"hidden_size": 1152, "depth": 24, "num_heads": 16},
            "fast_inference": {"hidden_size": 768, "depth": 12, "num_heads": 12},
            "memory_efficient": {"hidden_size": 512, "depth": 8, "num_heads": 8},
            "balanced": {"hidden_size": 1024, "depth": 20, "num_heads": 16}
        }
        if preset in vi_nex_presets:
            # Hacer merge profundo para nested dicts
            for key, value in vi_nex_presets[preset].items():
                if key in module and isinstance(module[key], dict) and isinstance(value, dict):
                    module[key].update(value)
                else:
                    module[key] = value
    
    return build_module(module, builder, **kwargs)


def build_vi_nex_ai_model(model_cfg: dict, model_type: str = "diffusion", preset: str = None, **kwargs):
    """
    Builder específico para modelos VI-NEX-AI con soporte para presets
    """
    registries = {
        "diffusion": MODELS,
        "vae": VAES,
        "dataset": DATASETS,
        "scheduler": SCHEDULERS,
        "optimizer": OPTIMIZERS
    }
    
    if model_type not in registries:
        available = list(registries.keys())
        raise ValueError(f"Tipo de modelo '{model_type}' no soportado. Opciones: {available}")
    
    return build_module_with_vi_nex_ai_preset(
        model_cfg, 
        registries[model_type], 
        preset=preset, 
        **kwargs
    )


# Inicializar componentes de VI-NEX-AI al importar el módulo
register_vi_nex_ai_components()