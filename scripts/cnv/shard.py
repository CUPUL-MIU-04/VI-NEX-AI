import os
import sys
from typing import List, Optional

import pandas as pd
from tqdm import tqdm

try:
    import dask.dataframe as dd
    SUPPORT_DASK = True
except ImportError:
    SUPPORT_DASK = False


def shard_parquet(input_path: str, k: int, columns_to_remove: Optional[List[str]] = None, 
                  output_dir: Optional[str] = None):
    """
    Dividir un archivo Parquet en múltiples fragmentos para VI-NEX-AI
    
    Args:
        input_path: Ruta al archivo Parquet de entrada
        k: Número de fragmentos a crear
        columns_to_remove: Columnas a eliminar (None para mantener todas)
        output_dir: Directorio de salida (None para usar directorio basado en nombre de archivo)
    """
    # Validar entrada
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Archivo de entrada {input_path} no existe.")
    
    if k <= 0:
        raise ValueError("El número de fragmentos (k) debe ser mayor a 0")

    # Leer archivo Parquet
    print(f"Leyendo {input_path}...")
    if SUPPORT_DASK:
        df = dd.read_parquet(input_path).compute()
    else:
        df = pd.read_parquet(input_path)

    print(f"Archivo cargado: {len(df)} filas, {len(df.columns)} columnas")

    # Eliminar columnas especificadas
    default_columns_to_remove = [
        "num_frames", "height", "width", "aspect_ratio", "fps", "resolution",
    ]
    
    if columns_to_remove is None:
        columns_to_remove = default_columns_to_remove
    
    columns_to_remove = [col for col in columns_to_remove if col in df.columns]
    
    if columns_to_remove:
        df = df.drop(columns=columns_to_remove)
        print(f"Columnas eliminadas: {columns_to_remove}")

    # Calcular tamaño de cada fragmento
    total_rows = len(df)
    rows_per_shard = (total_rows + k - 1) // k  # Redondeo hacia arriba

    # Crear directorio de salida
    if output_dir is None:
        base_dir = os.path.dirname(input_path)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_dir = os.path.join(base_dir, base_name + "_shards")
    
    os.makedirs(output_dir, exist_ok=True)
    print(f"Creando {k} fragmentos en: {output_dir}")

    # Crear y guardar fragmentos
    shard_info = []
    for i in tqdm(range(k), desc="Creando fragmentos"):
        start_idx = i * rows_per_shard
        end_idx = min(start_idx + rows_per_shard, total_rows)

        shard_df = df.iloc[start_idx:end_idx]
        if shard_df.empty:
            continue

        shard_file_name = f"{i:05d}.parquet"
        shard_path = os.path.join(output_dir, shard_file_name)

        shard_df.to_parquet(shard_path, index=False)
        shard_info.append({
            'shard_id': i,
            'file_name': shard_file_name,
            'rows': len(shard_df),
            'path': shard_path
        })

    # Guardar metadata de fragmentos
    shard_meta = pd.DataFrame(shard_info)
    shard_meta_path = os.path.join(output_dir, "shards_metadata.csv")
    shard_meta.to_csv(shard_meta_path, index=False)
    
    print(f"\nProceso completado:")
    print(f"  - Fragmentos creados: {len(shard_info)}")
    print(f"  - Filas por fragmento: ~{rows_per_shard}")
    print(f"  - Metadata guardada en: {shard_meta_path}")
    print(f"  - Total filas procesadas: {total_rows}")


def main():
    """Función principal para uso desde línea de comandos"""
    import argparse

    parser = argparse.ArgumentParser(description="Dividir archivos Parquet para VI-NEX-AI")
    parser.add_argument("input_path", type=str, help="Ruta al archivo Parquet de entrada")
    parser.add_argument("k", type=int, help="Número de fragmentos a crear", default=10000)
    parser.add_argument("--output-dir", type=str, help="Directorio de salida personalizado")
    parser.add_argument("--keep-all-columns", action="store_true", 
                       help="Mantener todas las columnas (no eliminar ninguna)")
    parser.add_argument("--columns-to-remove", nargs="+", 
                       help="Lista personalizada de columnas a eliminar")

    args = parser.parse_args()

    # Determinar columnas a eliminar
    if args.keep_all_columns:
        columns_to_remove = []
    elif args.columns_to_remove:
        columns_to_remove = args.columns_to_remove
    else:
        columns_to_remove = None  # Usar valores por defecto

    shard_parquet(
        input_path=args.input_path,
        k=args.k,
        columns_to_remove=columns_to_remove,
        output_dir=args.output_dir
    )


if __name__ == "__main__":